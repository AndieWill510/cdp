variable "project_name" { type = string }
variable "db_name" { type = string }
variable "db_username" { type = string }
variable "db_password" { type = string, sensitive = true }
variable "private_subnet_ids" { type = list(string) }
variable "vpc_id" { type = string }
variable "app_sg_id" { type = string }
