provider "aws" {
  region = "us-east-1"
}

data "aws_key_pair" "existing_deployer" {
  key_name = "DevOps"
}

resource "aws_iam_role" "ec2_role" {
  name = "ec2_role_devops"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      },
    ]
  })
}

# Using existing IAM policy
data "aws_iam_policy" "devops_node_policy" {
  name = "devops_node_policy"
}

resource "aws_iam_role_policy_attachment" "policy_attachment" {
  role       = aws_iam_role.ec2_role.name
  policy_arn = data.aws_iam_policy.devops_node_policy.arn
}

# Using existing IAM instance profile
data "aws_iam_instance_profile" "ec2_profile" {
  name = "ec2_profile"
}

# Using existing Security Group
data "aws_security_group" "devops_ec2_sg" {
  name = "devops_ec2_sg"
}

resource "aws_instance" "devops_ec2" {
  ami                  = "ami-0c7217cdde317cfec"
  instance_type        = "t2.xlarge"
  iam_instance_profile = data.aws_iam_instance_profile.ec2_profile.name
  security_groups      = [data.aws_security_group.devops_ec2_sg.name]
  key_name             = data.aws_key_pair.existing_deployer.key_name

  tags = {
    Name = "DevOps EC2 Instance"
  }

provisioner "local-exec" {
  command = <<EOF
    set -e
    RETRIES=3
    DELAY=10
    
    for i in $(seq 1 $RETRIES); do
      scp -i ${path.module}/DevOps.pem -o StrictHostKeyChecking=no -r ${path.module}/script ubuntu@${self.public_ip}:/home/ubuntu/ && break
      echo "Attempt $i failed! Waiting $DELAY seconds..."
      sleep $DELAY
    done

    for i in $(seq 1 $RETRIES); do
      scp -i ${path.module}/DevOps.pem -o StrictHostKeyChecking=no ${path.module}/.env ubuntu@${self.public_ip}:/home/ubuntu/ && break
      echo "Attempt $i failed! Waiting $DELAY seconds..."
      sleep $DELAY
    done

    for i in $(seq 1 $RETRIES); do
      scp -i ${path.module}/DevOps.pem -o StrictHostKeyChecking=no ${path.module}/requirements.txt ubuntu@${self.public_ip}:/home/ubuntu/ && break
      echo "Attempt $i failed! Waiting $DELAY seconds..."
      sleep $DELAY
    done

  EOF
  when    = create
}
  provisioner "remote-exec" {
    inline = [
      "git clone https://github.com/thisisarchimedes/devops.git",
      "./script/build_container.sh"
    ]
  }


  connection {
    type        = "ssh"
    user        = "ubuntu"
    private_key = file("${path.module}/DevOps.pem")
    host        = self.public_ip
  }
}
