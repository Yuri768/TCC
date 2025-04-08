const senhaInput = document.getElementById('senha');
    const confirmeSenhaInput = document.getElementById('confirme_senha');
    const erroSenha = document.getElementById('erro-senha');
    const submitBtn = document.getElementById('submit-btn');

    function validarSenhas() {
        if (senhaInput.value !== confirmeSenhaInput.value) {
            confirmeSenhaInput.classList.add('input-error');
            erroSenha.style.display = 'block';
            submitBtn.disabled = true;
        } else {
            confirmeSenhaInput.classList.remove('input-error');
            erroSenha.style.display = 'none';
            submitBtn.disabled = false;
        }
    }

    senhaInput.addEventListener('input', validarSenhas);
    confirmeSenhaInput.addEventListener('input', validarSenhas);

    document.querySelector('form').addEventListener('submit', function(event) {
        if (senhaInput.value !== confirmeSenhaInput.value) {
            event.preventDefault();
            confirmeSenhaInput.classList.add('input-error');
            erroSenha.style.display = 'block';
        }
    });