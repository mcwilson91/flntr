// # https://gist.github.com/DmytroLitvinov/39d9a1a93a46eb9da1e17d8e73f35e11
// # thanks to DmytroLitvinov for this code
//
// $(document).ready(function() {
//     function addMessage(text, extra_tags) {
//         var message = $(`
//             <div class="alert alert-dismissable alert-${extra_tags}">\n
//                 <a class="close" data-dismiss="alert" href="#">&times;</a>\n
//                     ${text}\n
//             </div>`).hide();
//         $("#messages").append(message);
//         message.fadeIn(500);
//
//         setTimeout(function() {
//             message.fadeOut(500, function() {
//                 message.remove();
//             });
//         }, 3000);
//     }
//
//     $(document).ajaxComplete(function (e, xhr, settings) {
//         var contentType = xhr.getResponseHeader("Content-Type");
//         if (contentType == "static/js") {
//             var json = $.evalJSON(xhr.responseText);
//             $.each(json.django_messages, function (i, item) {
//                 addMessage(item.text, item.tags);
//             });
//
//         }
//     }).ajaxError(function (e, xhr, settings, exception) {
//         addMessage("There was an error processing your request, please try again.", "error");
//     })
//
// });
