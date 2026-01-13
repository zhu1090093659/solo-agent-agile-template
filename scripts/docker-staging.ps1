# Staging Environment Docker Script (PowerShell)
# Usage: .\scripts\docker-staging.ps1 [up|down|build|logs]

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
    "-f", "docker/envs/staging.yml"
)

switch ($Command) {
    "up" {
        Write-Host "Starting staging environment..." -ForegroundColor Green
        & docker compose @ComposeFiles up -d @ExtraArgs
    }
    "down" {
        Write-Host "Stopping staging environment..." -ForegroundColor Yellow
        & docker compose @ComposeFiles down @ExtraArgs
    }
    "build" {
        Write-Host "Building staging images..." -ForegroundColor Cyan
        & docker compose @ComposeFiles build @ExtraArgs
    }
    "logs" {
        & docker compose @ComposeFiles logs @ExtraArgs
    }
}
