# Development Environment Docker Script (PowerShell)
# Usage: .\scripts\docker-dev.ps1 [up|down|build|logs]

param(
    [Parameter(Position=0)]
    [ValidateSet("up", "down", "build", "logs")]
    [string]$Command = "up",
    
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$ExtraArgs
)

$ComposeFiles = @(
    "-f", "docker/docker-compose.yml",
    "-f", "docker/docker-compose.frontend.yml",
    "-f", "docker/docker-compose.backend.yml",
    "-f", "docker/docker-compose.db.yml",
    "-f", "docker/envs/dev.yml"
)

switch ($Command) {
    "up" {
        Write-Host "Starting development environment..." -ForegroundColor Green
        & docker compose @ComposeFiles up @ExtraArgs
    }
    "down" {
        Write-Host "Stopping development environment..." -ForegroundColor Yellow
        & docker compose @ComposeFiles down @ExtraArgs
    }
    "build" {
        Write-Host "Building development images..." -ForegroundColor Cyan
        & docker compose @ComposeFiles build @ExtraArgs
    }
    "logs" {
        & docker compose @ComposeFiles logs @ExtraArgs
    }
}
