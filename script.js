+const box = document.getElementById('box');
const msgInput = document.getElementById('msg');
const sendBtn = document.getElementById('sendBtn');

// Lock input until Python engine finishes initialization
msgInput.disabled = true;
msgInput.placeholder = "Minima Engine loading... Please wait...";

function formatMarkdownText(text) {
  const regex = /```(\w*)\n([\s\S]*?)\n```/g;
  let matches = [];
  let match;

  while ((match = regex.exec(text)) !== null) {
    matches.push({
      full: match[0],
      lang: match[1],
      code: match[2],
      index: match.index,
    });
  }

  if (matches.length === 0) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML.replace(/\n/g, '<br>').replace(/  /g, '&nbsp;&nbsp;');
  }

  let lastIndex = 0;
  let resultHTML = '';

  matches.forEach((m) => {
    let plainText = text.substring(lastIndex, m.index);
    if (plainText) {
      const div = document.createElement('div');
      div.textContent = plainText;
      resultHTML += div.innerHTML.replace(/\n/g, '<br>').replace(/  /g, '&nbsp;&nbsp;');
    }

    const displayLang = m.lang || 'code';
    const divEscape = document.createElement('div');
    divEscape.textContent = m.code;
    const escapedCode = divEscape.innerHTML;

    resultHTML += `
      <div class="code-container">
          <div class="code-header">
              <span>${displayLang}</span>
              <button class="copy-btn" onclick="copyCode(this)">Copy</button>
          </div>
          <pre><code>${escapedCode}</code></pre>
      </div>
    `;
    lastIndex = m.index + m.full.length;
  });

  let remainingText = text.substring(lastIndex);
  if (remainingText) {
    const div = document.createElement('div');
    div.textContent = remainingText;
    resultHTML += div.innerHTML.replace(/\n/g, '<br>').replace(/  /g, '&nbsp;&nbsp;');
  }

  return resultHTML;
}

function copyCode(button) {
  const container = button.closest('.code-container');
  const codeText = container.querySelector('pre code').innerText;

  navigator.clipboard
    .writeText(codeText)
    .then(() => {
      button.innerText = 'Copied!';
      button.classList.add('copied');

      setTimeout(() => {
        button.innerText = 'Copy';
        button.classList.remove('copied');
      }, 2000);
    })
    .catch((err) => {
      console.error(err);
    });
}

window.copyCode = copyCode;

function appendMessage(text, isBot) {
  const bubble = document.createElement('div');
  bubble.className = isBot ? 'msg-bubble bot-msg' : 'msg-bubble user-msg';

  if (isBot) {
    bubble.innerHTML = formatMarkdownText(text);
  } else {
    bubble.textContent = text;
  }

  box.appendChild(bubble);
  box.scrollTop = box.scrollHeight;
}

function showLoadingIndicator() {
  const loader = document.createElement('div');
  loader.className = 'msg-bubble bot-msg loading-bubble';
  loader.id = 'chippy-loader';

  const textNode = document.createElement('span');
  textNode.id = 'loader-text';
  textNode.textContent = 'Thinking...';

  loader.appendChild(textNode);
  box.appendChild(loader);
  box.scrollTop = box.scrollHeight;

  const phrases = ['Thinking...', 'Cooking...', 'Modernizing...'];
  let index = 0;

  const intervalId = setInterval(() => {
    const element = document.getElementById('loader-text');
    if (element) {
      index = (index + 1) % phrases.length;
      element.textContent = phrases[index];
    } else {
      clearInterval(intervalId);
    }
  }, 1200);

  return intervalId;
}

function removeLoadingIndicator(intervalId) {
  clearInterval(intervalId);
  const loader = document.getElementById('chippy-loader');
  if (loader) {
    loader.remove();
  }
}

// Global functions exposed to Python
window.formatMarkdownText = formatMarkdownText;
window.showLoadingIndicator = showLoadingIndicator;
window.removeLoadingIndicator = removeLoadingIndicator;
window.appendMessage = appendMessage;

// Signal function Python will call when it is fully ready
window.pyEngineReady = function() {
  msgInput.disabled = false;
  msgInput.placeholder = "Message MINIMA...";
};
