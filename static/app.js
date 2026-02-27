async function postForm(formElement, endpoint) {
  const formData = new FormData(formElement);
  const response = await fetch(endpoint, {
    method: 'POST',
    body: formData,
  });

  const contentType = response.headers.get('Content-Type') || '';
  if (!response.ok) {
    if (contentType.includes('application/json')) {
      const err = await response.json();
      throw new Error(err.erro || 'Falha no processamento.');
    }
    throw new Error('Falha no processamento.');
  }

  return { response, contentType };
}

const formExtrair = document.getElementById('form-extrair');
const formRenomear = document.getElementById('form-renomear');

const statusExtrair = document.getElementById('status-extrair');
const statusRenomear = document.getElementById('status-renomear');

formExtrair.addEventListener('submit', async (event) => {
  event.preventDefault();
  statusExtrair.className = 'status warn';
  statusExtrair.textContent = 'Processando PDF...';

  try {
    const { response } = await postForm(formExtrair, '/api/extrair');
    const blob = await response.blob();

    const downloadName = (response.headers.get('Content-Disposition') || '')
      .split('filename=')[1]?.replaceAll('"', '') || 'Relatorio.xlsx';

    const url = URL.createObjectURL(blob);
    const anchor = document.createElement('a');
    anchor.href = url;
    anchor.download = downloadName;
    document.body.appendChild(anchor);
    anchor.click();
    anchor.remove();
    URL.revokeObjectURL(url);

    statusExtrair.className = 'status ok';
    statusExtrair.textContent = `Relatório gerado com sucesso: ${downloadName}`;
  } catch (error) {
    statusExtrair.className = 'status err';
    statusExtrair.textContent = error.message;
  }
});

formRenomear.addEventListener('submit', async (event) => {
  event.preventDefault();
  statusRenomear.className = 'status warn';
  statusRenomear.textContent = 'Lendo metadados do PDF...';

  try {
    const { response } = await postForm(formRenomear, '/api/renomear');
    const data = await response.json();

    statusRenomear.className = 'status ok';
    statusRenomear.innerHTML = `Novo nome sugerido: <strong>${data.novo_nome}</strong><br>
      <span class="badge">Ata ${data.numero_ata} • UG ${data.ug}</span>`;
  } catch (error) {
    statusRenomear.className = 'status err';
    statusRenomear.textContent = error.message;
  }
});
