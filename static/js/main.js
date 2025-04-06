document.addEventListener('DOMContentLoaded', () => {
    // Get elements
    const promptForm = document.getElementById('prompt-form');
    const promptInput = document.getElementById('prompt');
    const maxTokensInput = document.getElementById('max-tokens');
    const temperatureInput = document.getElementById('temperature');
    const temperatureValue = document.getElementById('temperature-value');
    const generateBtn = document.getElementById('generate-btn');
    const streamBtn = document.getElementById('stream-btn');
    const responseText = document.getElementById('response-text');
    const statusElement = document.getElementById('status');
    const modelInfoElement = document.getElementById('model-info');

    // Update parameter display
    temperatureInput.addEventListener('input', () => {
        temperatureValue.textContent = temperatureInput.value;
    });

    // Fetch model information
    async function fetchModelInfo() {
        try {
            const response = await fetch('/api/info');
            const data = await response.json();
            
            if (data.status === 'ready') {
                modelInfoElement.textContent = `Model: ${data.model} (Context Length: ${data.context_length})`;
            } else {
                modelInfoElement.textContent = 'Model: Loading or Unavailable';
                modelInfoElement.style.color = '#e74c3c';
            }
        } catch (error) {
            console.error('Failed to get model information:', error);
            modelInfoElement.textContent = 'Failed to get model information';
            modelInfoElement.style.color = '#e74c3c';
        }
    }

    // Call to standard generation API
    promptForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Input validation
        if (!promptInput.value.trim()) {
            alert('Please enter a prompt');
            return;
        }

        // Update UI
        generateBtn.disabled = true;
        streamBtn.disabled = true;
        responseText.textContent = 'Generating...';
        statusElement.textContent = '';
        
        // Prepare request data
        const requestData = {
            prompt: promptInput.value,
            max_tokens: parseInt(maxTokensInput.value),
            temperature: parseFloat(temperatureInput.value)
        };

        try {
            const startTime = Date.now();
            
            // API call
            const response = await fetch('/api/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(requestData)
            });

            const data = await response.json();
            const endTime = Date.now();
            
            if (data.error) {
                throw new Error(data.error);
            }

            // Display results
            responseText.textContent = data.generated_text;
            statusElement.textContent = `Tokens: ${data.tokens_generated} | 
                                        Generation time: ${data.inference_time_seconds}s | 
                                        Total time: ${((endTime - startTime) / 1000).toFixed(2)}s`;
        } catch (error) {
            console.error('Error:', error);
            responseText.textContent = `An error occurred: ${error.message}`;
            responseText.classList.add('error');
        } finally {
            // Restore UI state
            generateBtn.disabled = false;
            streamBtn.disabled = false;
        }
    });

    // Call to streaming API
    streamBtn.addEventListener('click', async () => {
        // Input validation
        if (!promptInput.value.trim()) {
            alert('Please enter a prompt');
            return;
        }

        // Update UI
        generateBtn.disabled = true;
        streamBtn.disabled = true;
        responseText.textContent = '';
        statusElement.textContent = 'Streaming...';
        
        // Prepare request data
        const requestData = {
            prompt: promptInput.value,
            max_tokens: parseInt(maxTokensInput.value),
            temperature: parseFloat(temperatureInput.value)
        };

        try {
            const startTime = Date.now();
            
            // Event source connection
            const eventSource = new EventSource(`/api/generate_stream?${new URLSearchParams({
                prompt: requestData.prompt,
                max_tokens: requestData.max_tokens,
                temperature: requestData.temperature
            })}`);
            
            // Message event handler
            eventSource.onmessage = (event) => {
                if (event.data === '[DONE]') {
                    // Streaming complete
                    eventSource.close();
                    const endTime = Date.now();
                    statusElement.textContent = `Streaming complete | Total time: ${((endTime - startTime) / 1000).toFixed(2)}s`;
                    generateBtn.disabled = false;
                    streamBtn.disabled = false;
                } else {
                    // Add text
                    responseText.textContent += event.data;
                }
            };
            
            // Error handler
            eventSource.onerror = (error) => {
                console.error('Streaming error:', error);
                eventSource.close();
                responseText.classList.add('error');
                statusElement.textContent = 'A streaming error occurred';
                generateBtn.disabled = false;
                streamBtn.disabled = false;
            };
        } catch (error) {
            console.error('Error:', error);
            responseText.textContent = `An error occurred: ${error.message}`;
            responseText.classList.add('error');
            generateBtn.disabled = false;
            streamBtn.disabled = false;
        }
    });

    // Fetch model info on page load
    fetchModelInfo();
});