$(document).ready(function () {
    $('#result-table').DataTable({
        "pagingType": "first_last_numbers" // "simple" option for 'Previous' and 'Next' buttons only
    });
    $('.dataTables_length').addClass('bs-select');
});