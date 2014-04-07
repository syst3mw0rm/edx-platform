function sendLog(name, data, event_type) {
  var message = data || {};
  message.chapter = PDF_URL || '';
  message.name = "textbook.pdf." + name;
  Logger.log(event_type ? event_type : message.name, message);
};

// this event is loaded after the others to accurately represent the order of events:
// click next -> pagechange
$(function() {
  var first_page = true;
  var curr_page = 1;

  $(window).bind("pagechange", function(event) {
    // log every page render
    var page = event.originalEvent.pageNumber;
    // pagechange is called many times per viewing.
    if (PDFView.previousPageNumber !== page || first_page) {
      first_page = false;
      sendLog("page.loaded", {"type": "gotopage", "old": PDFView.previousPageNumber, "new": page}, "book");
      setTimeout(function(){curr_page = page}, 250);
    }
  });

  $('#viewerContainer').bind('DOMMouseScroll mousewheel', function(event) {
    scrolled_page = PDFView.page;
    if (scrolled_page != curr_page) {
      curr_page = PDFView.page;
      var direction = PDFView.pageViewScroll.down ? "down" : "up";
      sendLog("page.scrolled", {"page": curr_page, "direction": direction});
    }
  });
});

// this is called too often
// $(window).bind('pagerender', function(event) {
//   var message = {
//       "current": event.originalEvent.detail.pageNumber
//     };
//   sendLog("page.display", message);
// });

$('#viewThumbnail,#sidebarToggle').on('click', function() {
    sendLog("thumbnails.toggled", {"page": PDFView.page});
  });

$('#thumbnailView a').live('click', function(){
  sendLog("thumbnail.navigated", {"title": $(this).attr("title")});
});

$('#viewOutline').on('click', function() {
    sendLog("outline.toggled", {"page": PDFView.page});
  });

$('#previous').on('click', function() {
    sendLog("page.navigatednext", {"type": "prevpage", "new": PDFView.page - 1}, "book");
  });

$('#next').on('click', function() {
    sendLog("page.navigatednext", {"type": "nextpage", "new": PDFView.page + 1}, "book");
  });

$('#zoomIn,#zoomOut').on('click', function() {
    sendLog("zoom.changed", {"zoomtype": "button", "direction": $(this).attr("id")});
  });

$('#pageNumber').on('change', function() {
    sendLog("page.navigated", {"page": $(this).val()});
  });

var old_amount = 1;
$(window).bind('scalechange', function(evt) {
  var amount = evt.originalEvent.scale;
  if (amount !== old_amount) {
    sendLog("display.scaled", {"amount": amount});
    old_amount = amount;
  }
});

$('#scaleSelect').on('change', function() {
  sendLog("zoom.changed", {"zoomtype": "menu", "amount": $("#scaleSelect").val()});
});

$(window).bind("find findhighlightallchange findagain findcasesensitivitychange", function(event) {
  setTimeout(function(){
    var message = event.originalEvent.detail;
    message.action = event.type;
    message.status = $('#findMsg').text();
    sendLog("search", message);
  }, 400);
});
