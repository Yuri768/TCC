document.addEventListener('DOMContentLoaded', () => {
    let currentStep = 1;
    let selected = {
        servico: null,
        medico: null,
        data: null,
        horario: null
    };

    // Step 1: Seleção de Serviço
    document.getElementById('select-servico').addEventListener('change', async (e) => {
        selected.servico = e.target.value;
        if (selected.servico) {
            const response = await fetch(`/agendamento/get_medicos/?servico_id=${selected.servico}`);
            document.getElementById('select-medico').innerHTML = await response.text();
            document.getElementById('select-medico').disabled = false;
            currentStep = 2;
            updateSteps();
        }
    });

    // Step 2: Seleção de Médico
    document.getElementById('select-medico').addEventListener('change', (e) => {
        selected.medico = e.target.value;
        if (selected.medico) {
            initCalendar();
            currentStep = 3;
            updateSteps();
        }
    });

    // Step 3: Seleção de Data
    function initCalendar() {
        // Implementação completa do calendário com validação de datas
        // (Código similar ao anterior, adaptado para buscar horários via AJAX)
    }

    // Step 4: Seleção de Horário
    function loadHorarios(data) {
        // Implementação para carregar horários via AJAX
    }

    function updateSteps() {
        document.querySelectorAll('.step').forEach((step, index) => {
            step.classList.toggle('active', index < currentStep);
        });
    }

    // Implementações restantes do calendário e validações...
});