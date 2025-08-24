# Caminho para seu repositório
$RepoPath = 'C:\source\IAResipa'
Set-Location $RepoPath

# Garanta que não haja nada pendente
git status

# Faça backup em caso de problemas
git branch backup-before-filter

# Use git filter-branch para eliminar a pasta do histórico
git filter-branch --index-filter `
  "git rm -r --cached --ignore-unmatch '04.deploy/docker/backup_atual'" `
  --prune-empty --tag-name-filter cat -- --all

# Limpeza pós-reescrita
Remove-Item -Recurse -Force .git/refs/original/
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Force push para atualizar o remoto (ATENÇÃO: reescreve histórico!)
git push origin --force --all
git push origin --force --tags
