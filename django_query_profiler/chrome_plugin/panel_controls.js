/**
 * This function is used to clear data in html table, called when the user
 * clicks the clear data button
 */
var clearTableData = function () {
	var tableHeaderRowCount = 1;
	var table = document.getElementById('panel_table_id');

	var rowCount = table.rows.length - 1;  // -1 because of footer
	for (var i = tableHeaderRowCount; i < rowCount ; i++) {
		table.deleteRow(tableHeaderRowCount);
	}
};


document.addEventListener('DOMContentLoaded', function () {
	var button = document.getElementById('panel_table_body_clear_button');
	button.addEventListener('click', function () {
		clearTableData();
	});

	var exportToExcelButton = document.getElementById('export-to-excel');
	exportToExcelButton.addEventListener('click', function () {
		fnExcelReport()

	});

});


/**
 * Copied from
 * i) http://stackoverflow.com/questions/22317951/export-html-table-data-to-excel-using-javascript-jquery-is-not-working-properl
 * ii) http://stackoverflow.com/questions/7034754/how-to-set-a-file-name-using-window-open
 */
function fnExcelReport() {
	var tab_text = "<table border='2px'><tr bgcolor='#87AFC6'>";
	var table = document.getElementById('panel_table_id');

	for (var j = 0; j < table.rows.length; j++) {
		tab_text = tab_text + table.rows[j].innerHTML + "</tr>";
	}

	tab_text = tab_text + "</table>";
	tab_text = tab_text.replace(/<A[^>]*>|<\/A>/g, "");//remove if u want links in your table
	tab_text = tab_text.replace(/<img[^>]*>/gi, ""); // remove if u want images in your table
	tab_text = tab_text.replace(/<input[^>]*>|<\/input>/gi, ""); // reomves input params

	var uri = 'data:application/vnd.ms-excel,' + encodeURIComponent(tab_text);
	var downloadLink = document.createElement("a");
	downloadLink.href = uri;
	downloadLink.download = "django_query_profiled_data.xls";

	document.body.appendChild(downloadLink);
	downloadLink.click();
	document.body.removeChild(downloadLink);
}
