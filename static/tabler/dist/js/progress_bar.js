htmx.on('#filterform', 'htmx:xhr:progress', function (evt) {
    htmx.find('#progress').setAttribute('aria-valuenow', evt.detail.loaded / evt.detail.total * 100);
    htmx.find('#progress').style.width = evt.detail.loaded / evt.detail.total * 100 + "%";
});