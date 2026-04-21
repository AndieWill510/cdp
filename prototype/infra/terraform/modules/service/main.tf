resource "aws_ecs_cluster" "this" {
  name = "${var.project_name}-cluster"
}

resource "aws_iam_role" "task_execution" {
  name = "${var.project_name}-task-execution-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole",
      Principal = { Service = "ecs-tasks.amazonaws.com" },
      Effect = "Allow"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "task_execution" {
  role       = aws_iam_role.task_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_ecs_task_definition" "api" {
  family                   = "${var.project_name}-api"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "512"
  memory                   = "1024"
  execution_role_arn       = aws_iam_role.task_execution.arn

  container_definitions = jsonencode([{
    name      = "api",
    image     = var.container_image,
    essential = true,
    portMappings = [{
      containerPort = 8000,
      hostPort      = 8000,
      protocol      = "tcp"
    }],
    environment = [
      { name = "APP_ENV", value = "aws" },
      { name = "SYNC_DATABASE_URL", value = "postgresql://${var.db_username}:${var.db_password}@${var.db_host}:5432/${var.db_name}" },
      { name = "DATABASE_URL", value = "postgresql+psycopg://${var.db_username}:${var.db_password}@${var.db_host}:5432/${var.db_name}" }
    ],
    command = ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
  }])
}

resource "aws_ecs_service" "api" {
  name            = "${var.project_name}-api"
  cluster         = aws_ecs_cluster.this.id
  task_definition = aws_ecs_task_definition.api.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    assign_public_ip = true
    subnets          = var.public_subnet_ids
    security_groups  = [var.app_sg_id]
  }
}

output "service_name" { value = aws_ecs_service.api.name }
