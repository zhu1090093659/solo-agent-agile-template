# Production Environment Docker Script (PowerShell)
# Usage: .\scripts\docker-prod.ps1 [up|down|build|logs]
#
# Required environment variables:
#   SECRET_KEY    - Application secret key
#   DB_USER       - Database username
#   DB_PASSWORD   - Database password
#   DB_NAME       - Database name

param(
    [Parameter(Position=0)]
    [ValidateSet("up", "down", "build", "logs")]
    [string]$Command = "up",
    
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$ExtraArgs
)

# Check required environment variables
$RequiredVars = @("SECRET_KEY", "DB_USER", "DB_PASSWORD", "DB_NAME")
$MissingVars = @()

foreach ($var in $RequiredVars) {
    if (-not [Environment]::GetEnvironmentVariable($var)) {
        $MissingVars += $var
    }
}

if ($MissingVars.Count -gt 0) {
    Write-Host "Error: Required environment variables not set." -ForegroundColor Red
    Write-Host "Missing: $($MissingVars -join ', ')" -ForegroundColor Red
    exit 1
}

$ComposeFiles = @(
    "-f", "docker/docker-compose.yml",
    "-f", "docker/docker-compose.frontend.yml",
    "-f", "docker/docker-compose.backend.yml",
    "-f", "docker/docker-compose.db.yml",
    "-f", "docker/envs/prod.yml"
)

switch ($Command) {
    "up" {
        Write-Host "Starting production environment..." -ForegroundColor Green
        & docker compose @ComposeFiles up -d @ExtraArgs
    }
    "down" {
        Write-Host "Stopping production environment..." -ForegroundColor Yellow
        & docker compose @ComposeFiles down @ExtraArgs
    }
    "build" {
        Write-Host "Building production images..." -ForegroundColor Cyan
        & docker compose @ComposeFiles build @ExtraArgs
    }
    "logs" {
        & docker compose @ComposeFiles logs @ExtraArgs
    }
}
