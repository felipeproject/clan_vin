:reload

@echo off

:: Adicione as alterações ao staging
git add .

:: Faça um commit com uma mensagem padrão
git commit -m "Atualizações feitas"

:: Envie as alterações para o repositório remoto
git push origin main

:: Para repositórios em outras branches, substitua "main" pelo nome da sua branch
:: git push origin sua-branch

echo Atualização concluída!

goto:reload