
terraform {
  required_version = ">= 0.12"
}

resource "aws_iam_role" "FooBar" {
  name = join("-", [var.foo, "role1"])

  assume_role_policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
    {
        "Action": "sts:AssumeRole",
        "Principal": {
        "Service": "ec2.amazonaws.com"
        },
        "Effect": "Allow",
        "Sid": ""
    }
    ]
}
EOF
}

resource "aws_iam_role" "foo-bar" {
  name = join("-", [var.foo, "role2"])

  assume_role_policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
    {
        "Action": "sts:AssumeRole",
        "Principal": {
        "Service": "ec2.amazonaws.com"
        },
        "Effect": "Allow",
        "Sid": ""
    }
    ]
}
EOF
}

resource "aws_iam_policy" "FooBaz" {
  name        = var.foo
  description = "A test policy"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "ec2:Describe*"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
EOF
}

locals {
  resource_map = {
    resource1 = aws_iam_role.role1.name
    resource2 = aws_iam_role.role2.name
  }
}


resource "aws_iam_role_policy_attachment" "foo-baz" {
  for_each = local.resource_map

  role       = each.value
  policy_arn = aws_iam_policy.policy.arn
}


module "FooBin" {
  source  = "git@github.com:rackspace-infrastructure-automation/test//modules/terraform?ref=v1.2.3"

  param1 = "some_string"
  param2 = 1234
  param3 = true
  param4 = ["some_other_string", 5678, false, aws_iam_role2.name]

  param5 = {
    subparam1 = "one more string"
    subparam2 = 9876
  }

  param7 = aws_iam_policy.role1.name
}

module "foo-bin" {
  source  = "git@github.com:rackspace-infrastructure-automation/test//modules/terraform?ref=v1.2.3"

  param1 = "some_string"
  param2 = 1234
  param3 = true
  param4 = ["some_other_string", 5678, false, aws_iam_role2.name]

  param5 = {
    subparam1 = "one more string"
    subparam2 = 9876
  }

  param7 = aws_iam_policy.role1.name
}
