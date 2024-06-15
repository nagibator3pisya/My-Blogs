 document.getElementById('cancelButton').addEventListener('click', function () {
    document.getElementById('statusField').value = 'draft';
    document.getElementById('articleForm').submit();
 });