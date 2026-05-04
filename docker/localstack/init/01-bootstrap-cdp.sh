#!/usr/bin/env bash
set -euo pipefail

# CDP LocalStack bootstrap
#
# LocalStack runs scripts mounted into /etc/localstack/init/ready.d after the
# LocalStack runtime is ready. This script creates the local AWS-like resources
# used by docker/docker-compose.yml.

AWS_REGION="${AWS_REGION:-${AWS_DEFAULT_REGION:-us-east-1}}"
ENDPOINT_URL="${AWS_ENDPOINT_URL:-http://localhost:4566}"

export AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID:-test}"
export AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY:-test}"
export AWS_DEFAULT_REGION="${AWS_REGION}"

awslocal_cmd() {
  if command -v awslocal >/dev/null 2>&1; then
    awslocal "$@"
  else
    aws --endpoint-url "${ENDPOINT_URL}" "$@"
  fi
}

create_bucket() {
  local bucket_name="$1"
  echo "Creating S3 bucket: ${bucket_name}"
  awslocal_cmd s3 mb "s3://${bucket_name}" >/dev/null 2>&1 || true
}

create_queue() {
  local queue_name="$1"
  local redrive_policy="${2:-}"

  echo "Creating SQS queue: ${queue_name}"
  if [[ -n "${redrive_policy}" ]]; then
    awslocal_cmd sqs create-queue \
      --queue-name "${queue_name}" \
      --attributes "${redrive_policy}" >/dev/null
  else
    awslocal_cmd sqs create-queue \
      --queue-name "${queue_name}" >/dev/null
  fi
}

put_parameter() {
  local name="$1"
  local value="$2"
  echo "Writing SSM parameter: ${name}"
  awslocal_cmd ssm put-parameter \
    --name "${name}" \
    --type String \
    --value "${value}" \
    --overwrite >/dev/null
}

put_secret() {
  local name="$1"
  local value="$2"
  echo "Writing Secrets Manager secret: ${name}"
  awslocal_cmd secretsmanager create-secret \
    --name "${name}" \
    --secret-string "${value}" >/dev/null 2>&1 \
    || awslocal_cmd secretsmanager put-secret-value \
      --secret-id "${name}" \
      --secret-string "${value}" >/dev/null
}

# S3 buckets
create_bucket "cdp-evidence-local"
create_bucket "cdp-artifacts-local"
create_bucket "cdp-exports-local"

# SQS queues
create_queue "cdp-dead-letter-queue"

DLQ_URL="$(awslocal_cmd sqs get-queue-url --queue-name cdp-dead-letter-queue --query QueueUrl --output text)"
DLQ_ARN="$(awslocal_cmd sqs get-queue-attributes --queue-url "${DLQ_URL}" --attribute-names QueueArn --query 'Attributes.QueueArn' --output text)"
REDRIVE_POLICY="RedrivePolicy={\"deadLetterTargetArn\":\"${DLQ_ARN}\",\"maxReceiveCount\":\"3\"}"

create_queue "cdp-intake-queue" "${REDRIVE_POLICY}"
create_queue "cdp-review-queue" "${REDRIVE_POLICY}"
create_queue "cdp-execution-queue" "${REDRIVE_POLICY}"
create_queue "cdp-appeal-queue" "${REDRIVE_POLICY}"
create_queue "cdp-repair-queue" "${REDRIVE_POLICY}"

# EventBridge bus
EVENT_BUS_NAME="cdp-events-local"
echo "Creating EventBridge bus: ${EVENT_BUS_NAME}"
awslocal_cmd events create-event-bus --name "${EVENT_BUS_NAME}" >/dev/null 2>&1 || true

# Optional DynamoDB table for idempotency / lightweight locks.
echo "Creating DynamoDB table: cdp-idempotency-local"
awslocal_cmd dynamodb create-table \
  --table-name cdp-idempotency-local \
  --attribute-definitions AttributeName=idempotency_key,AttributeType=S \
  --key-schema AttributeName=idempotency_key,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST >/dev/null 2>&1 || true

# SSM parameters
put_parameter "/cdp/local/database-url" "postgresql+psycopg://cdp:cdp@postgres:5432/cdp"
put_parameter "/cdp/local/qdrant-url" "http://qdrant:6333"
put_parameter "/cdp/local/redis-url" "redis://redis:6379/0"
put_parameter "/cdp/local/default-policy-profile" "local-dev"
put_parameter "/cdp/local/event-bus-name" "${EVENT_BUS_NAME}"

# Secrets. These are local-only defaults and must never be used in production.
put_secret "/cdp/local/signing-key" "local-dev-signing-key-change-me"
put_secret "/cdp/local/database-password" "cdp"

echo "CDP LocalStack bootstrap complete."
