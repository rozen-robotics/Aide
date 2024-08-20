/**
 * App Chat
 */

'use strict';

document.addEventListener('DOMContentLoaded', function () {
    (function () {
        const chatHistoryBody = document.querySelector('.chat-history-body');

        // Initialize PerfectScrollbar for chat history
        if (chatHistoryBody) {
            const ps = new PerfectScrollbar(chatHistoryBody, {
                wheelPropagation: false,
                suppressScrollX: true
            });
        }

        // Scroll to bottom function
        function scrollToBottom() {
            chatHistoryBody.scrollTo(0, chatHistoryBody.scrollHeight);
        }

        scrollToBottom();

    })();

    let chatHistory = []; // Переменная для хранения истории чата

    const chatForm = document.getElementById('chat-form');

    chatForm.addEventListener('submit', async function (event) {
        event.preventDefault();

        const userInput = document.getElementById('user-input').value;
        if (!userInput.trim()) return;

        const user_image_path = document.querySelector('#user-image-path').value;
        const ai_image_path = document.querySelector('#ai-image-path').value;

        const messagesElement = document.getElementById('messages');
        const loaderElement = document.getElementById('loader');

        // Добавляем сообщение пользователя в чат и в историю
        const userMessage = document.createElement('li');
        userMessage.className = 'chat-message chat-message-right';
        userMessage.innerHTML = `
                <div class="d-flex overflow-hidden">
                    <div class="chat-message-wrapper flex-grow-1">
                        <div class="chat-message-text">
                            <p class="mb-0 text-white">${userInput}</p>
                        </div>
                    </div>
                    <div class="user-avatar flex-shrink-0 ms-4">
                        <div class="avatar avatar-sm">
                            <img src="${user_image_path}" alt="Avatar" class="rounded-circle">
                        </div>
                    </div>
                </div>
            `;
        messagesElement.appendChild(userMessage);
        messagesElement.scrollTop = messagesElement.scrollHeight;

        // Очищаем поле ввода
        document.getElementById('user-input').value = '';

        // Обновляем историю чата
        chatHistory.push({role: 'user', content: userInput});

        // Показываем индикатор загрузки
        loaderElement.style.display = 'block';

        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        try {
            const response = await fetch('/multimedia/process_question_ajax/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({
                    request_type: 'question_answering',
                    text: `Вот история чата: ${chatHistory.map(entry => `${entry.role}: ${entry.content}`).join(' ')}`
                })
            });

            const data = await response.json();

            // Скрываем индикатор загрузки
            loaderElement.style.display = 'none';
            // Добавляем ответ AI в чат и в историю
            const aiMessage = document.createElement('li');
            aiMessage.className = 'chat-message';
            aiMessage.innerHTML = `
                    <div class="d-flex overflow-hidden">
                        <div class="user-avatar flex-shrink-0 me-4">
                            <div class="avatar avatar-sm">
                                <img src="${ai_image_path}" alt="AI avatar" class="rounded-circle">
                            </div>
                        </div>
                        <div class="chat-message-wrapper flex-grow-1">
                            <div class="chat-message-text">
                                <p class="mb-0">${data.response || data.error || 'No response'}</p>
                            </div>
                        </div>
                    </div>
                `;
            messagesElement.appendChild(aiMessage);
            messagesElement.scrollTop = messagesElement.scrollHeight;

            // Обновляем историю чата
            chatHistory.push({role: 'ai', content: data.response});
        } catch (error) {
            // Скрываем индикатор загрузки
            loaderElement.style.display = 'none';

            // Добавляем сообщение об ошибке в чат
            const errorMessage = document.createElement('li');
            errorMessage.className = 'chat-message text-danger';
            errorMessage.innerHTML = `
                    <div class="d-flex overflow-hidden">
                        <div class="chat-message-wrapper flex-grow-1">
                            <div class="chat-message-text">
                                <p class="mb-0">Error: ${error.message}</p>
                            </div>
                        </div>
                    </div>
                `;
            messagesElement.appendChild(errorMessage);
            messagesElement.scrollTop = messagesElement.scrollHeight;

            // Обновляем историю чата
            chatHistory.push({role: 'error', content: error.message});
        }
    });
});
