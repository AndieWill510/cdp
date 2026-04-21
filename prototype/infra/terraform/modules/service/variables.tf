variable "project_name" { type = string }
variable "aws_region" { type = string }
variable "vpc_id" { type = string }
variable "public_subnet_ids" { type = list(string) }
variable "app_sg_id" { type = string }
variable "container_image" { type = string }
variable "db_host" { type = string }
variable "db_name" { type = string }
variable "db_username" { type = string }
variable "db_password" { type = string, sensitive = true }
