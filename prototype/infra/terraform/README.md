# Terraform scaffold

This is an intentionally lean AWS scaffold for productionizing the prototype.

## What it creates

- VPC with public/private subnets
- Security groups
- RDS PostgreSQL
- ECS cluster + Fargate service for API
- ECR repository placeholders

## Commands

```bash
terraform init
terraform plan \
  -var="project_name=cdp" \
  -var="db_password=REPLACE_ME"
terraform apply \
  -var="project_name=cdp" \
  -var="db_password=REPLACE_ME"
```

## Notes

- Replace the placeholder task image with your pushed container image
- Add secrets manager, ALB auth, IAM hardening, and CI/CD before serious use
