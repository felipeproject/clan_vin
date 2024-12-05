:reload

@echo off
color 61
:: Adicione as alterações ao staging
git add .
color 69
:: Faça um commit com uma mensagem padrão
git commit -m "Atualizações feitas"
color 61
:: Envie as alterações para o repositório remoto
git push origin main
color 69
:: Para repositórios em outras branches, substitua "main" pelo nome da sua branch
:: git push origin sua-branch
color 61
echo Atualização concluída!

cls
color 1
pause
goto:reload