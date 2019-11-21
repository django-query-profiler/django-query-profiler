/** This variable is initialized as soon as the panel is created.
 * This is the only way to grab the reference to the window, and then add/remove stuff
 */
var PanelWindow;

/**
 * This function creates a new panel in devtools
 */
chrome.devtools.panels.create(
	"Django Query Profiler",
	null,
	"panel_table.html",
	function (extensionPanel) {
		extensionPanel.onShown.addListener(
			function (panelWindow) {
				PanelWindow = panelWindow;
				panelWindow.addEventListener('DOMContentLoaded', function () {
					var button = PanelWindow.document.getElementById('panel_table_body_clear_button');
					button.addEventListener('click', function () {
						clearTableData();
					});
				});
			}
		);
	}
);

/** @namespace chrome.devtools.network.onRequestFinished */
/**
 * This is the listener which grabs the {dbStats, dbStatsUrl, servert_time} and
 * calls a function to add these elements to PanelWindow.
 */
chrome.devtools.network.onRequestFinished.addListener(
	function (har_entry) {
		var responseHeaders = har_entry.response.headers;
		var found = false;
		for (var i = 0; i < responseHeaders.length; i++) {
			var responseHeader = responseHeaders[i];
			var headerName = responseHeader.name;
			if (headerName.toUpperCase() == 'X-QUERY_PROFILER_SUMMARY_DATA') {
				var dbStatsObj = JSON.parse(responseHeader.value);
				found = true;
			} else if (headerName.toUpperCase() == 'X-QUERY_PROFILER_DETAILED_URL') {
				var dbStatsUrl = responseHeader.value;
				found = true;
			} else if (headerName.toUpperCase() == 'X-TOTAL_SERVER_TIME_IN_MILLIS') {
				var serverTimeInMillis = responseHeader.value;
				found = true;
			} else if (headerName.toUpperCase() == 'X-TIME_SPENT_PROFILING_IN_MICROS') {
				var profilingTimeInMicros = responseHeader.value;
				found = true;
			} else if (headerName.toUpperCase() == 'X-QUERY_PROFILER_TYPE') {
				var queryProfilerType = responseHeader.value;
				found = true;
			}

		}

		if (found) {
			var url = har_entry.request.url;
			var apiName = getPathName(url);
			dbStatsUrl += '?name=' + apiName;
			var tableNode = PanelWindow.document.getElementById('panel_table_id');
			var requestTime = Math.floor(har_entry.time);
			createRowAndAppend(tableNode, apiName, requestTime,
				dbStatsObj, dbStatsUrl, serverTimeInMillis, profilingTimeInMicros, queryProfilerType);
		}
	}
);

/**
 * This function creates a new node in the PanelWindow - with apiName, dbStatus and dbStatsUrl
 * It grabs the PanelWindow object and creates new html elements
 */
var createRowAndAppend = function (tableNode, apiName, requestTime, dbStatsObj, dbStatsUrl, serverTimeInMillis,
								   profilingTimeInMicros, queryProfilerType) {

	// PART 1: Finding table and creating tr
	var tr = document.createElement('tr');

	addTd(tr, apiName, 'wrappedClass');
	addTd(tr, commafy(requestTime));
	addTd(tr, commafy(serverTimeInMillis));
	addTd(tr, commafy(profilingTimeInMicros/1000));
	addTd(tr, commafy(dbStatsObj.total_query_execution_time_in_micros/1000));

	addTd(tr, commafy(dbStatsObj.SELECT));
	addTd(tr, commafy(dbStatsObj.INSERT));
	addTd(tr, commafy(dbStatsObj.UPDATE));
	addTd(tr, commafy(dbStatsObj.DELETE));
	addTd(tr, commafy(dbStatsObj.TRANSACTIONALS));
	addTd(tr, commafy(dbStatsObj.OTHER));

	addTd(tr, commafy(dbStatsObj.total_db_row_count));
	addTd(tr, dbStatsObj.potential_n_plus1_query_count);
	addTd(tr, dbStatsObj.exact_query_duplicates);
	addAnchorLink(tr, dbStatsUrl, queryProfilerType);
	tableNode.appendChild(tr);
};


/**
 * This function is a helper function to know path of a url.  Copied from stackoverflow.
 */
var getPathName = function (href) {
	var l = document.createElement("a");
	l.href = href;
	return l.pathname;
};


/**
 * A helper function to add a td to the tr.  It checks for presence of the value
 */
var addTd = function (tr, value, className) {
	var td = document.createElement('td');
	if (className) {
		td.className = className;
	}

	var div = document.createElement('div');
	var divValue = document.createTextNode(value == undefined ? '-' : value);
	div.appendChild(divValue);
	td.appendChild(div);
	tr.appendChild(td);
};

/**
 * This function adds a anchor link to the tr
 */
var addAnchorLink = function(tr, value, queryProfilerType) {
	var td = document.createElement('td');
	var div = document.createElement('div');
	var anchorTag = document.createElement('a');
	anchorTag.setAttribute('href', value);
	anchorTag.setAttribute('target', '_blank');
	if (queryProfilerType == 'QUERY') {
		anchorTag.innerHTML = 'query';
	} else {
		anchorTag.innerHTML = 'query_signature';
	}
	div.appendChild(anchorTag);
	td.appendChild(div);
	tr.appendChild(td);
};

/**
 * For putting comma after every three digits
 * Ignoring the decimal values since the value is in milliseconds.  Copied from stackoverflow
 */
var commafy = function (num) {
	if (num == undefined) {
		return '-';
	}

	var str = num.toString().split('.');
	if (str[0].length >= 4) {
		str[0] = str[0].replace(/(\d)(?=(\d{3})+$)/g, '$1,');
	}
	if (str[1] && str[1].length >= 4) {
		str[1] = str[1].replace(/(\d{3})/g, '$1 ');
	}
	return str.join('.');
};
