document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("chat-form").addEventListener("submit", async function (event) {
        event.preventDefault();
        
        // 사용자 입력 값 가져오기
        const container = document.getElementById('container');
        const userInputElement = document.getElementById("user-input");
        const userInput = userInputElement.value;
        const chatBox = document.getElementById('response');
        const sendBtn = document.getElementById("find_query");

        // 입력이 없으면 경고 메시지 표시
        if (!userInput && !userInputElement.disabled) {
            alert("질문을 입력해주세요!");
            return; 
        }
        
        // 사용자 질문을 화면에 추가
        const userMessage = document.createElement("div");
        userMessage.classList.add("userInput");
        userMessage.textContent = userInput;
        chatBox.appendChild(userMessage);

        // 입력창 초기화
        userInputElement.value = "";
        container.scrollTop = container.scrollHeight;

        // 로딩 메시지 표시 + 로딩 박스가 보이도록 설정
        const loading = document.getElementById("loadingBox");
        userInputElement.disabled = true;
        sendBtn.disabled = true; // sendBtn 비활성화
        loading.style.display = 'block'; 

        container.scrollTop = container.scrollHeight;

        try {
            // 서버에 답변 요청 보내기
            const response = await fetch("/retrieve", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ text: userInput }),
            });

            // 응답 확인
            if (!response.ok) {
                throw new Error("서버 응답이 올바르지 않습니다.");
            }

            // 답변 받아오기 + 로딩 박스 안보이도록 설정
            const data = await response.json();
            loading.style.display = "none"; 

            // 한 글자씩 타이핑 효과로 답변 추가
            const responseMessage = document.createElement("div");
            responseMessage.classList.add("response-item");
            responseMessage.innerHTML = '<span class="response-icon"><i class="fas fa-atom"></i></span>';
            chatBox.appendChild(responseMessage);

            let i = 0;
            const text = data.text;
            const typeWriter = () => {
                if (i < text.length) {
                    responseMessage.innerHTML += text.charAt(i);
                    i++;
                    setTimeout(typeWriter, 20); 
                } else {
                    userInputElement.disabled = false;
                    sendBtn.disabled = false; // sendBtn 다시 활성화
                    container.scrollTop = container.scrollHeight; 
                }
            };
            typeWriter();

        } catch (error) {
            // 에러 발생 시 처리
            alert("오류가 발생했습니다. 다시 시도해주세요.");
            userInputElement.disabled = false;
            sendBtn.disabled = false; // sendBtn 다시 활성화
            loading.style.display = 'none';  
        }

    });
});
