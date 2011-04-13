function CustomFileBrowser(field_name, url, type, win) {
    
    var cmsURL = "/admin/filebrowser/browse/?pop=2";
    cmsURL = cmsURL + "&type=" + type;
    
    tinyMCE.activeEditor.windowManager.open({
        file: cmsURL,
        width: 820,  // Your dimensions may differ - toy around with them!
        height: 500,
        resizable: "yes",
        scrollbars: "yes",
        inline: "no",  // This parameter only has an effect if you use the inlinepopups plugin!
        close_previous: "no",
    }, {
        window: win,
        input: field_name,
        editor_id: tinyMCE.selectedInstance.editorId,
    });
    return false;
}


tinyMCE.init({
    // main settings
    mode: "exact",
    elements: "id_description",
    content_css: "/media/style/tinymce/content.css",
    theme: "advanced",
    language: "en",
    skin: "grappelli",
    browsers: "msie,gecko,safari",
    dialog_type: "window",
    editor_deselector : "mceNoEditor",
    
    // general settings
    width: '700',
    height: '300',
    indentation : '10px',
    fix_list_elements : true,
    relative_urls: false,
    remove_script_host : true,
    accessibility_warnings : false,
    object_resizing: true,
    cleanup_on_startup: true,
    //forced_root_block: "p",
    remove_trailing_nbsp: true,
    
    // callbackss
    file_browser_callback: "CustomFileBrowser",
    
    // theme_advanced
    theme_advanced_toolbar_location: "top",
    theme_advanced_toolbar_align: "left",
    theme_advanced_statusbar_location: "bottom",
    theme_advanced_buttons1: "bold,italic|,bullist,numlist,blockquote,|,undo,redo,|,link,unlink,|,image,media,pasteword,template,charmap,|,code,|,cleanup",
    theme_advanced_buttons2: "grappelli_documentstructure",
    theme_advanced_buttons3: "",
    theme_advanced_path: false,
    theme_advanced_blockformats: "p,h2,h3,h4,pre,blockquote",
    theme_advanced_resizing : true,
    theme_advanced_resize_horizontal : false,
    theme_advanced_resizing_use_cookie : true,
    theme_advanced_styles: "",
    advlink_styles: "intern=internal;extern=external",
    
    // plugins
    plugins: "advimage,advlink,paste,media,searchreplace,grappelli,template",
    advimage_update_dimensions_onchange: true,
    
    // grappelli settings
    grappelli_adv_hidden: false,
    grappelli_show_documentstructure: "on",
    
    // templates
    template_templates : [
        {
            title : "Symmetrical 2 Columns.",
            src : "/tinymce/template/2col/",
            description : "Symmetrical 2 Columns."
        },
        {
            title : "Asymmetrical 2 Columns (big right)",
            src : "/tinymce/template/2col/bigright/",
            description : "Asymmetrical 2 Columns: big left, small right."
        },
        {
            title : "Asymmetrical 2 Columns (big left)",
            src : "/tinymce/template/2col/bigleft/",
            description : "Asymmetrical 2 Columns: big left, small right."
        },
    ],
    
    // elements
    valid_elements : ""
    + "-p,"
    + "a[href|title],"
    + "-strong/-b,"
    + "-em/-i,"
    + "-ol,"
    + "-ul,"
    + "-li,"
    + "img[src|alt=|width|height]," + 
    + "-h2,-h3,-h4," + 
    + "-pre," +
    + "-blockquote," +
    + "-code," + 
    + "div",
    
    extended_valid_elements: ""
    + "-blockquote,"
    + "a[href|title],"
    + "img[class|src|border=0|alt|title|hspace|vspace|width|height|align|onmouseover|onmouseout|name],"
    + "-p[class<clearfix?summary?code],"
    + "h2[class<clearfix],h3[class<clearfix],h4[class<clearfix],"
    + "-ul[class<clearfix],-ol[class<clearfix],"
    + "div[class],"
    + "object[align<bottom?left?middle?right?top|archive|border|class|classid"
      + "|codebase|codetype|data|declare|dir<ltr?rtl|height|hspace|id|lang|name"
      + "|onclick|ondblclick|onkeydown|onkeypress|onkeyup|onmousedown|onmousemove"
      + "|onmouseout|onmouseover|onmouseup|standby|style|tabindex|title|type|usemap"
      + "|vspace|width],"
    +"param[id|name|type|value|valuetype<DATA?OBJECT?REF],",

    valid_child_elements : ""
    + "h1/h2/h3/h4/h5/h6/a[%itrans_na],"
    + "table[thead|tbody|tfoot|tr|td],"
    + "blockquote[p|ul|ol|table|h3|h4|h5|h6],"
    + "div[%btrans|%itrans|#text],"
    + "strong/p/em/td[%itrans|#text],"
    + "body[%btrans|#text]",
});
