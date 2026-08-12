#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# Deploy del repository RPDindexOptimized su GitHub
#
# Repository storico di riferimento:
#   https://github.com/marcorighi/RPDindex
#   https://doi.org/10.5281/zenodo.20313771
#
# Nuovo repository:
#   https://github.com/marcorighi/RPDindexOptimized
#
# Requisiti:
#   - git
#   - GitHub CLI (gh)
#   - autenticazione eseguita con: gh auth login
#
# Eseguire questo script dalla directory radice del NUOVO progetto.
# ============================================================

OWNER="marcorighi"
REPO_NAME="RPDindexOptimized"
FULL_REPO="${OWNER}/${REPO_NAME}"
REMOTE_URL="https://github.com/${FULL_REPO}.git"

DESCRIPTION="Optimized implementation of the RPD indices, preserving the semantics of the original RPDindex software."

DEFAULT_COMMIT_MESSAGE="Initial public version of RPDindexOptimized"

die() {
    echo "ERRORE: $*" >&2
    exit 1
}

command -v git >/dev/null 2>&1 || die "git non trovato."
command -v gh  >/dev/null 2>&1 || die "GitHub CLI (gh) non trovato."

echo "==> Verifica autenticazione GitHub..."
gh auth status >/dev/null 2>&1 || die \
    "GitHub CLI non autenticato. Eseguire prima: gh auth login"

echo "==> Directory corrente:"
pwd

# Evita per errore il deploy dalla directory del vecchio repository.
CURRENT_BASENAME="$(basename "$PWD")"
if [[ "$CURRENT_BASENAME" == "RPDindex" ]]; then
    die "La directory corrente sembra essere il vecchio repository RPDindex. Eseguire lo script dalla directory del nuovo progetto."
fi

echo "==> Inizializzazione repository Git locale..."
if [[ ! -d .git ]]; then
    git init
fi

git branch -M main

echo "==> Configurazione remote origin..."

if git remote get-url origin >/dev/null 2>&1; then
    EXISTING_ORIGIN="$(git remote get-url origin)"

    if [[ "$EXISTING_ORIGIN" != "$REMOTE_URL" && \
          "$EXISTING_ORIGIN" != "git@github.com:${FULL_REPO}.git" ]]; then
        echo
        echo "ATTENZIONE: esiste già un remote 'origin':"
        echo "  $EXISTING_ORIGIN"
        echo
        die "Non modifico automaticamente un origin differente. Verificarlo manualmente."
    fi
else
    if gh repo view "$FULL_REPO" >/dev/null 2>&1; then
        echo "    Il repository GitHub esiste già."
        git remote add origin "$REMOTE_URL"
    else
        echo "    Creo il repository pubblico GitHub: $FULL_REPO"
        gh repo create "$FULL_REPO" \
            --public \
            --description "$DESCRIPTION" \
            --source=. \
            --remote=origin
    fi
fi

echo "==> Stato prima del commit:"
git status --short

echo "==> Aggiunta dei file..."
git add -A

if git diff --cached --quiet; then
    echo "==> Nessuna modifica da committare."
else
    COMMIT_MESSAGE="${1:-$DEFAULT_COMMIT_MESSAGE}"
    echo "==> Commit:"
    echo "    $COMMIT_MESSAGE"
    git commit -m "$COMMIT_MESSAGE"
fi

echo "==> Push su GitHub..."
git push -u origin main

echo
echo "Deploy completato."
echo
echo "Repository:"
echo "  https://github.com/${FULL_REPO}"
echo
echo "Repository originale di riferimento:"
echo "  https://github.com/marcorighi/RPDindex"
echo "  https://doi.org/10.5281/zenodo.20313771"
echo
echo "Ultimo commit locale:"
git log -1 --oneline
