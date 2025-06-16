document.addEventListener('DOMContentLoaded', function() {
    // Dados fictícios
    // Dados dos médicos (sem precisar especificar a imagem)
    const medicosPorEspecialidade = {
        'cardiologia': [
            { id: 1, nome: 'Carlos Silva', especialidade: 'Cardiologista' },
            { id: 2, nome: 'Ana Souza', especialidade: 'Cardiologista Pediátrica' }
        ],
        'dermatologia': [
            { id: 3, nome: 'Marcos Oliveira', especialidade: 'Dermatologista' },
            { id: 4, nome: 'Juliana Costa', especialidade: 'Dermatologista Estética' }
        ],
        'ortopedia': [
            { id: 5, nome: 'Roberto Santos', especialidade: 'Ortopedista' }
        ],
        'pediatria': [
            { id: 6, nome: 'Patricia Lima', especialidade: 'Pediatra' },
            { id: 7, nome: 'Fernando Rocha', especialidade: 'Neonatologista' }
        ]
    };

    function formatarNomeArquivo(nome) {
        return nome
            .toLowerCase()                   // Tudo em minúsculo
            .normalize('NFD')                // Remove acentos
            .replace(/[\u0300-\u036f]/g, '') // Remove caracteres especiais
            .replace(/\s+/g, '_')            // Substitui espaços por _
            .replace(/[^\w_]/g, '');         // Remove outros caracteres especiais
    }



    // Horários disponíveis
    const horariosDisponiveis = [
        '08:00', '09:00', '10:00', '11:00', 
        '14:00', '15:00', '16:00', '17:00'
    ];

    // Estado da aplicação
    const state = {
        currentStep: 1,
        selected: {
            servico: null,
            medico: null,
            data: null,
            horario: null
        },
        calendar: {
            month: new Date().getMonth(),
            year: new Date().getFullYear()
        }
    };

    // Elementos DOM
    const elements = {
        steps: document.querySelectorAll('.step'),
        stepIndicators: document.querySelectorAll('.step-indicator'),
        serviceCards: document.querySelectorAll('.service-card'),
        doctorOptions: document.getElementById('doctor-options'),
        currentMonth: document.getElementById('current-month'),
        calendarGrid: document.getElementById('calendar'),
        prevMonth: document.getElementById('prev-month'),
        nextMonth: document.getElementById('next-month'),
        timeSlots: document.getElementById('time-slots'),
        confirmBtn: document.getElementById('confirm-btn'),
        summary: {
            service: document.getElementById('summary-service'),
            doctor: document.getElementById('summary-doctor'),
            date: document.getElementById('summary-date'),
            time: document.getElementById('summary-time')
        }
    };

    // Inicialização
    init();

    function init() {
        renderCalendar();
        setupEventListeners();
        updateUI();
    }

    function setupEventListeners() {
        // Seleção de serviço
        elements.serviceCards.forEach(card => {
            card.addEventListener('click', function() {
                elements.serviceCards.forEach(c => c.classList.remove('selected'));
                this.classList.add('selected');
                state.selected.servico = this.dataset.service;
                state.currentStep = 2;
                renderDoctors();
                updateUI();
            });
        });

        // Navegação do calendário
        elements.prevMonth.addEventListener('click', function() {
            state.calendar.month--;
            if (state.calendar.month < 0) {
                state.calendar.month = 11;
                state.calendar.year--;
            }
            renderCalendar();
        });

        elements.nextMonth.addEventListener('click', function() {
            state.calendar.month++;
            if (state.calendar.month > 11) {
                state.calendar.month = 0;
                state.calendar.year++;
            }
            renderCalendar();
        });

        // Botão de confirmação
        elements.confirmBtn.addEventListener('click', function() {
            if (validateSelection()) {
                alert(`Agendamento confirmado!\n\nServiço: ${state.selected.servico}\nMédico: ${state.selected.medico}\nData: ${formatDate(state.selected.data)}\nHorário: ${state.selected.horario}`);
                // Aqui você adicionaria a lógica para enviar para o backend
            }
        });
    }

    function renderDoctors() {
    if (!state.selected.servico) return;

    const medicos = medicosPorEspecialidade[state.selected.servico] || [];
    elements.doctorOptions.innerHTML = '';

    medicos.forEach(medico => {
        const nomeArquivo = formatarNomeArquivo(medico.nome);
        const imgPath = `/static/img/${nomeArquivo}.jpg`;
        
        const doctorCard = document.createElement('div');
        doctorCard.className = 'doctor-card';
        doctorCard.innerHTML = `
            <img src="${imgPath}" alt="${medico.nome}" 
                 onerror="this.src='/static/img/padrao.jpg'">
            <div class="doctor-info">
                <h3>${medico.nome}</h3>
                <p>${medico.especialidade}</p>
            </div>
        `;
        
        doctorCard.addEventListener('click', function() {
            document.querySelectorAll('.doctor-card').forEach(c => c.classList.remove('selected'));
            this.classList.add('selected');
            state.selected.medico = medico.nome;
            state.currentStep = 3;
            updateUI();
        });
        
        elements.doctorOptions.appendChild(doctorCard);
    });
}

    function renderCalendar() {
        const { month, year } = state.calendar;
        const monthNames = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                          "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"];
        
        elements.currentMonth.textContent = `${monthNames[month]} ${year}`;
        
        const firstDay = new Date(year, month, 1);
        const lastDay = new Date(year, month + 1, 0);
        const daysInMonth = lastDay.getDate();
        
        elements.calendarGrid.innerHTML = '';
        
        // Dias vazios no início
        for (let i = 0; i < firstDay.getDay(); i++) {
            const emptyDay = document.createElement('div');
            emptyDay.className = 'calendar-day empty';
            elements.calendarGrid.appendChild(emptyDay);
        }
        
        // Dias do mês
        const today = new Date();
        for (let day = 1; day <= daysInMonth; day++) {
            const date = new Date(year, month, day);
            const dayElement = document.createElement('div');
            dayElement.className = 'calendar-day';
            dayElement.textContent = day;
            
            // Verificar se é hoje
            if (date.getDate() === today.getDate() && 
                date.getMonth() === today.getMonth() && 
                date.getFullYear() === today.getFullYear()) {
                dayElement.classList.add('today');
            }
            
            // Desabilitar dias passados
            if (date < new Date(today.getFullYear(), today.getMonth(), today.getDate())) {
                dayElement.classList.add('disabled');
            } else {
                dayElement.addEventListener('click', function() {
                    document.querySelectorAll('.calendar-day').forEach(d => d.classList.remove('selected'));
                    this.classList.add('selected');
                    state.selected.data = date;
                    state.currentStep = 4;
                    renderTimeSlots();
                    updateUI();
                });
            }
            
            // Marcar dia selecionado
            if (state.selected.data && 
                state.selected.data.getDate() === day && 
                state.selected.data.getMonth() === month && 
                state.selected.data.getFullYear() === year) {
                dayElement.classList.add('selected');
            }
            
            elements.calendarGrid.appendChild(dayElement);
        }
    }

    function renderTimeSlots() {
        if (!state.selected.data) return;

        elements.timeSlots.innerHTML = '';
        
        horariosDisponiveis.forEach(horario => {
            const timeSlot = document.createElement('div');
            timeSlot.className = 'time-slot';
            timeSlot.textContent = horario;
            
            timeSlot.addEventListener('click', function() {
                document.querySelectorAll('.time-slot').forEach(t => t.classList.remove('selected'));
                this.classList.add('selected');
                state.selected.horario = horario;
                updateUI();
            });
            
            elements.timeSlots.appendChild(timeSlot);
        });
    }

    function updateUI() {
        // Atualizar indicadores de passo
        elements.stepIndicators.forEach((indicator, index) => {
            if (index < state.currentStep) {
                indicator.classList.add('active');
            } else {
                indicator.classList.remove('active');
            }
        });

        // Mostrar apenas o passo atual
        elements.steps.forEach(step => {
            if (parseInt(step.dataset.step) === state.currentStep) {
                step.classList.add('active');
            } else {
                step.classList.remove('active');
            }
        });

        // Atualizar resumo
        elements.summary.service.textContent = state.selected.servico || 'Não selecionado';
        elements.summary.doctor.textContent = state.selected.medico || 'Não selecionado';
        elements.summary.date.textContent = state.selected.data ? formatDate(state.selected.data) : 'Não selecionada';
        elements.summary.time.textContent = state.selected.horario || 'Não selecionado';

        // Habilitar/desabilitar botão de confirmação
        elements.confirmBtn.disabled = !validateSelection();

        document.querySelectorAll('.btn-voltar').forEach(btn => {
            btn.style.display = state.currentStep > 1 ? 'flex' : 'none';
        });
    }

    function validateSelection() {
        return state.selected.servico && 
               state.selected.medico && 
               state.selected.data && 
               state.selected.horario;
    }

    function formatDate(date) {
        if (!date) return '';
        const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
        return date.toLocaleDateString('pt-BR', options);
    }
});

function voltarEtapa() {
    if (state.currentStep > 1) {
        state.currentStep--;
        updateUI();
        
        // Rolando para o topo do passo
        document.querySelector(`.step[data-step="${state.currentStep}"]`).scrollIntoView({
            behavior: 'smooth'
        });
    }
}