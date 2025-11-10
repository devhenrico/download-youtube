let formatoSelecionado = 'mp4';

// Selecionar formato
document.querySelectorAll('.format-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        document.querySelectorAll('.format-btn').forEach(b => b.classList.remove('active'));
        this.classList.add('active');
        formatoSelecionado = this.dataset.format;
    });
});

async function baixarVideo() {
    const url = document.getElementById('url').value.trim();
    const statusDiv = document.getElementById('status');
    const loader = document.getElementById('loader');
    const downloadBtn = document.querySelector('.download-btn');

    if (!url) {
        mostrarStatus('❌ Por favor, insira uma URL válida!', 'error');
        return;
    }

    // Desabilitar botão e mostrar loading
    downloadBtn.disabled = true;
    loader.style.display = 'block';
    statusDiv.style.display = 'none';

    try {
        mostrarStatus('🔄 Processando download...', 'loading');

        const response = await fetch('/download', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                url: url,
                formato: formatoSelecionado
            })
        });

        const data = await response.json();

        if (data.success) {
            mostrarStatus('✅ Download concluído! Iniciando transferência...', 'success');
            
            // Fazer download do arquivo
            window.location.href = `/download-file/${data.filename}`;
            
            // Limpar o campo de URL
            document.getElementById('url').value = '';
            
            setTimeout(() => {
                statusDiv.style.display = 'none';
            }, 3000);
        } else {
            mostrarStatus(`❌ Erro: ${data.error}`, 'error');
        }
    } catch (error) {
        mostrarStatus(`❌ Erro: ${error.message}`, 'error');
    } finally {
        loader.style.display = 'none';
        downloadBtn.disabled = false;
    }
}

function mostrarStatus(mensagem, tipo) {
    const statusDiv = document.getElementById('status');
    statusDiv.textContent = mensagem;
    statusDiv.className = `status ${tipo}`;
    statusDiv.style.display = 'block';
}

// Enter para baixar
document.getElementById('url').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        baixarVideo();
    }
});
