output "public_ip" {
  description = "The public IP for ssh access"
  value       = aws_instance.app_server.public_ip
}
