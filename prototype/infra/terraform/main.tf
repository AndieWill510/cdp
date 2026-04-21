module "network" {
  source       = "./modules/network"
  project_name = var.project_name
  aws_region   = var.aws_region
}

module "postgres" {
  source             = "./modules/postgres"
  project_name       = var.project_name
  db_name            = var.db_name
  db_username        = var.db_username
  db_password        = var.db_password
  private_subnet_ids = module.network.private_subnet_ids
  vpc_id             = module.network.vpc_id
  app_sg_id          = module.network.app_sg_id
}

module "service" {
  source             = "./modules/service"
  project_name       = var.project_name
  aws_region         = var.aws_region
  vpc_id             = module.network.vpc_id
  public_subnet_ids  = module.network.public_subnet_ids
  app_sg_id          = module.network.app_sg_id
  container_image    = var.container_image
  db_host            = module.postgres.db_address
  db_name            = var.db_name
  db_username        = var.db_username
  db_password        = var.db_password
}
