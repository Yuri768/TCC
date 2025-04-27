// Dados das consultas (simulando um banco de dados)
const consultas = [
    {
        id: 1,
        medico: "Dr. Carlos Silva",
        tipo: "Cardiologia",
        data: "15/05/2023 - 14:30",
        status: "completed",
        descricao: "Consulta de rotina para acompanhamento cardíaco."
    },
    {
        id: 2,
        medico: "Dra. Ana Paula",
        tipo: "Ginecologia",
        data: "20/06/2023 - 10:00",
        status: "pending",
        descricao: "Consulta de rotina anual."
    },
    {
        id: 3,
        medico: "Dr. Marcos Oliveira",
        tipo: "Ortopedia",
        data: "05/07/2023 - 16:15",
        status: "pending",
        descricao: "Avaliação de dor no joelho direito."
    },
    {
        id: 4,
        medico: "Dra. Juliana Costa",
        tipo: "Pediatria",
        data: "12/04/2023 - 09:00",
        status: "completed",
        descricao: "Acompanhamento de crescimento."
    },
    {
        id: 5,
        medico: "Dr. Roberto Almeida",
        tipo: "Cirurgia Geral",
        data: "28/05/2023 - 11:30",
        status: "cancelled",
        descricao: "Pré-operatório para cirurgia de hérnia."
    },
    {
        id: 6,
        medico: "Dra. Fernanda Lima",
        tipo: "Dermatologia",
        data: "10/08/2023 - 15:45",
        status: "pending",
        descricao: "Avaliação de manchas na pele."
    }
];

// Elementos do DOM
const consultasContainer = document.getElementById('consultasContainer');
const cancelModal = document.getElementById('cancelModal');
const closeModal = document.getElementById('closeModal');
const cancelCancel = document.getElementById('cancelCancel');
const cancelForm = document.getElementById('cancelForm');
const motivoInput = document.getElementById('motivo');
const consultaIdInput = document.getElementById('consultaId');

// Função para renderizar as consultas
function renderConsultas() {
    consultasContainer.innerHTML = '';
    
    consultas.forEach(consulta => {
        const card = document.createElement('div');
        card.className = 'consulta-card';
        
        // Determinar classe de status e texto
        let statusClass, statusText;
        switch(consulta.status) {
            case 'completed':
                statusClass = 'status-completed';
                statusText = 'Realizada';
                break;
            case 'pending':
                statusClass = 'status-pending';
                statusText = 'Agendada';
                break;
            case 'cancelled':
                statusClass = 'status-cancelled';
                statusText = 'Cancelada';
                break;
        }
        
        card.innerHTML = `
            <div class="consulta-header">
                <h3 class="consulta-title">${consulta.tipo}</h3>
                <span class="consulta-status ${statusClass}">${statusText}</span>
            </div>
            <div class="consulta-details">
                <div class="detail-row">
                    <span class="detail-label">Médico:</span>
                    <span class="detail-value">${consulta.medico}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Data:</span>
                    <span class="detail-value">${consulta.data}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Descrição:</span>
                    <span class="detail-value">${consulta.descricao}</span>
                </div>
            </div>
            <div class="consulta-actions">
                <button class="btn btn-download" ${consulta.status !== 'completed' ? 'disabled' : ''}>
                    <i class="fas fa-download"></i> Baixar Documentos
                </button>
                <button class="btn btn-cancel" ${consulta.status !== 'pending' ? 'disabled' : ''} data-id="${consulta.id}">
                    <i class="fas fa-times"></i> Cancelar
                </button>
            </div>
        `;
        
        consultasContainer.appendChild(card);
    });
    
    // Adicionar eventos aos botões de cancelar
    document.querySelectorAll('.btn-cancel:not(:disabled)').forEach(btn => {
        btn.addEventListener('click', () => openCancelModal(btn.dataset.id));
    });
}

// Função para abrir o modal de cancelamento
function openCancelModal(id) {
    consultaIdInput.value = id;
    motivoInput.value = '';
    cancelModal.style.display = 'flex';
}

// Função para fechar o modal
function closeCancelModal() {
    cancelModal.style.display = 'none';
}

// Função para cancelar uma consulta
function cancelarConsulta(id, motivo) {
    const consultaIndex = consultas.findIndex(c => c.id == id);
    if (consultaIndex !== -1) {
        consultas[consultaIndex].status = 'cancelled';
        consultas[consultaIndex].motivoCancelamento = motivo;
        renderConsultas();
        alert(`Consulta cancelada com sucesso. Motivo: ${motivo}`);
    }
    closeCancelModal();
}

// Event Listeners
closeModal.addEventListener('click', closeCancelModal);
cancelCancel.addEventListener('click', closeCancelModal);

cancelForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const motivo = motivoInput.value.trim();
    if (motivo) {
        cancelarConsulta(consultaIdInput.value, motivo);
    } else {
        alert('Por favor, informe o motivo do cancelamento.');
    }
});

// Fechar modal ao clicar fora do conteúdo
cancelModal.addEventListener('click', (e) => {
    if (e.target === cancelModal) {
        closeCancelModal();
    }
});


// Controle do menu mobile
const menuToggle = document.getElementById('menuToggle');
const sidebar = document.querySelector('.sidebar');

menuToggle.addEventListener('click', (e) => {
    e.stopPropagation(); // Impede a propagação do evento
    sidebar.classList.toggle('active');
    menuToggle.classList.toggle('active');
    
    // Alterna entre ícone de menu e X
    if (sidebar.classList.contains('active')) {
        menuToggle.innerHTML = '<i class="fas fa-times"></i>';
    } else {
        menuToggle.innerHTML = '<i class="fas fa-bars"></i>';
    }
});

// Fechar menu ao clicar fora
document.addEventListener('click', (e) => {
    if (window.innerWidth <= 768 && 
        !sidebar.contains(e.target) && 
        e.target !== menuToggle) {
        sidebar.classList.remove('active');
        menuToggle.classList.remove('active');
        menuToggle.innerHTML = '<i class="fas fa-bars"></i>';
    }
});

// Fechar menu ao clicar em um item
document.querySelectorAll('.sidebar-menu a').forEach(item => {
    item.addEventListener('click', () => {
        if (window.innerWidth <= 768) {
            sidebar.classList.remove('active');
            menuToggle.classList.remove('active');
            menuToggle.innerHTML = '<i class="fas fa-bars"></i>';
        }
    });
});

// Inicializar a página
document.addEventListener('DOMContentLoaded', renderConsultas);