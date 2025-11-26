function selectComponent(n) {
    fetch(`/select/${n}`).then(() => updateStatus());
}

function toggleComponent(n) {
    fetch(`/toggle/${n}`).then(() => setTimeout(updateStatus, 500));
}

function killAll() {
    fetch(`/kill_all`).then(() => setTimeout(updateStatus, 500));
}

function updateStatus() {
    fetch("/").then(resp => resp.text()).then(html => {
        document.body.innerHTML = html;
    });
}

// Optional: auto-refresh indicators every 5s
setInterval(updateStatus, 5000);

