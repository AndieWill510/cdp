variable "project_name" {
  type = string
}

variable "aws_region" {
  type    = string
  default = "us-west-2"
}

variable "db_password" {
  type      = string
  sensitive = true
}

variable "db_username" {
  type    = string
  default = "cdp"
}

variable "db_name" {
  type    = string
  default = "cdp"
}

variable "container_image" {
  type    = string
  default = "public.ecr.aws/docker/library/python:3.12-slim"
}
