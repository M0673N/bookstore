variable "SECRET_KEY" {
  description = "Secret key for the Django application."
}

variable "EMAIL_HOST_PASSWORD" {
  description = "Email host password."
}

variable "EMAIL_HOST_USER" {
  description = "Email host user."
}

variable "EMAIL_HOST" {
  description = "Email host address."
}

variable "EMAIL_PORT" {
  description = "Email port."
  type        = number
}

variable "EMAIL_USE_TLS" {
  description = "Use TLS for email."
  type        = bool
}

variable "CLOUDINARY_NAME" {
  description = "Cloudinary name."
}

variable "CLOUDINARY_API_KEY" {
  description = "Cloudinary API key."
}

variable "CLOUDINARY_API_SECRET" {
  description = "Cloudinary API secret."
}

variable "POSTGRES_DATABASE" {
  description = "PostgreSQL database name."
}

variable "POSTGRES_USERNAME" {
  description = "PostgreSQL username."
}

variable "POSTGRES_PASSWORD" {
  description = "PostgreSQL password."
}

variable "POSTGRES_HOST" {
  description = "PostgreSQL host."
}

variable "SITE_OWNER_EMAIL" {
  description = "Site owner email address."
}
