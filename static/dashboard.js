function selectComponent(n) {
    fetch(`/select/${n}`);
}

function toggleComponent(n) {
    fetch(`/toggle/${n}`);
}

function killAll() {
    fetch(`/kill_all`);
}

