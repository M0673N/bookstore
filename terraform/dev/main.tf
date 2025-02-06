terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "3.0.2"
    }
  }
}

provider "docker" {
  host = "npipe:////./pipe/dockerDesktopLinuxEngine" # For Docker Desktop on Windows
}

resource "docker_volume" "data" {
  name = "bookstore_data"
}

resource "docker_volume" "static_volume" {
  name = "bookstore_static_volume"
}

resource "docker_network" "app_network" {
  name = "bookstore_network"
}

resource "docker_container" "database" {
  name    = "database"
  image   = "postgres"
  restart = "always"

  mounts {
    source = docker_volume.data.name
    target = "/var/lib/postgresql/data/"
    type   = "volume"
  }

  networks_advanced {
    name = docker_network.app_network.name
  }

  healthcheck {
    test     = ["CMD-SHELL", "pg_isready -U ${var.POSTGRES_USERNAME} -d ${var.POSTGRES_DATABASE}"]
    interval = "10s"
    timeout  = "5s"
    retries  = 5
  }

  wait = true

  env = [
    "POSTGRES_USER=${var.POSTGRES_USERNAME}",
    "POSTGRES_PASSWORD=${var.POSTGRES_PASSWORD}",
    "POSTGRES_DB=${var.POSTGRES_DATABASE}"
  ]
}

resource "docker_container" "app" {
  name    = "app"
  image   = "m0673n/bookstore"
  restart = "always"

  mounts {
    source = docker_volume.static_volume.name
    target = "/bookstore/staticfiles"
    type   = "volume"
  }

  depends_on = [docker_container.database]

  networks_advanced {
    name = docker_network.app_network.name
  }

  healthcheck {
    test     = ["CMD-SHELL", "/bin/sh -c 'curl --fail http://localhost:8000 || exit 1'"]
    interval = "10s"
    timeout  = "5s"
    retries  = 3
  }

  wait = true

  env = [
    "SECRET_KEY=${var.SECRET_KEY}",
    "EMAIL_HOST=${var.EMAIL_HOST}",
    "EMAIL_HOST_USER=${var.EMAIL_HOST_USER}",
    "EMAIL_HOST_PASSWORD=${var.EMAIL_HOST_PASSWORD}",
    "EMAIL_PORT=${var.EMAIL_PORT}",
    "EMAIL_USE_TLS=${var.EMAIL_USE_TLS}",
    "CLOUDINARY_NAME=${var.CLOUDINARY_NAME}",
    "CLOUDINARY_API_KEY=${var.CLOUDINARY_API_KEY}",
    "CLOUDINARY_API_SECRET=${var.CLOUDINARY_API_SECRET}",
    "POSTGRES_DATABASE=${var.POSTGRES_DATABASE}",
    "POSTGRES_USERNAME=${var.POSTGRES_USERNAME}",
    "POSTGRES_PASSWORD=${var.POSTGRES_PASSWORD}",
    "POSTGRES_HOST=${var.POSTGRES_HOST}",
    "SITE_OWNER_EMAIL=${var.SITE_OWNER_EMAIL}"
  ]
}

resource "docker_container" "nginx" {
  name  = "nginx"
  image = "nginx"

  ports {
    internal = 80
    external = 80
  }

  mounts {
    source = docker_volume.static_volume.name
    target = "/bookstore/staticfiles"
    type   = "volume"
  }

  mounts {
    source = abspath("./nginx.conf")
    target = "/etc/nginx/nginx.conf"
    type   = "bind"
  }

  depends_on = [docker_container.app]

  networks_advanced {
    name = docker_network.app_network.name
  }
}

resource "docker_container" "mailhog" {
  name  = "mailhog"
  image = "mailhog/mailhog"

  ports {
    internal = 1025
    external = 1025
  }

  ports {
    internal = 8025
    external = 8025
  }

  networks_advanced {
    name = docker_network.app_network.name
  }
}
