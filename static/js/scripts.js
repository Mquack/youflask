function confirmDelete() {
  return confirm("Are you sure you want to delete this file?");
}

function openRenameModal(video) {
  document.getElementById('oldNameInput').value = video;
  document.getElementById('renameModal').style.display = 'block';
}

function closeRenameModal() {
  document.getElementById('renameModal').style.display = 'none';
}
