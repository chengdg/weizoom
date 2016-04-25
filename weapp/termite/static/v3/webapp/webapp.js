/**
 * alertEditTemplateLinkTarget: 提示用户在“模板”中进行配置
 */
W.alertEditTemplateLinkTarget = function() {
    /*
    $('body').alert({
        isShow: true,
        speed: 3000,
        info: '请在后台管理系统中，点击"模板"--"编辑"，编辑链接目标'
    });
    */
}

/**
 * interceptLinkClick: 拦截点击链接的行为，加上project_id参数
 */
W.interceptLinkClick = function() {
	$('a').click(function(event) {
	    var $link = $(event.currentTarget);
	    var href = $link.attr('href');
	    if ((href[0] === '/') || (href.indexOf('?') !== -1)) {
	        if ((href.indexOf('project_id=') === -1) && W.projectId) {
	            href = (href + '&project_id=' + W.projectId);
	        }
	    }

	    $link.attr('href', href);
	});
}

W.showVisitHistory = function(title, url) {
    $('<div>').simpledialog2({
        mode: 'button',
        headerText: '前往之前查看页面',
        headerClose: false,
        buttonPrompt: title,
        zindex: 9999,
        buttons : {
          '是': {
            click: function () { 
              $('#buttonoutput').text('是');
              redirectTo(url);
            }
          },
          '否': {
            click: function () { 
              $('#buttonoutput').text('否');
            },
            icon: "delete",
            theme: "c"
          }
        }
    });
}


W.preloadImgsOnPage = function(ele) {
    $(function(){
        if (!ele) {
            console.log(ele)
            return;
        }
        var $itemsImg = $(ele);
        $itemsImg.map(function(idx, item) {
            $item = $(item);
            $item.attr('data-url', $item.attr('src'));
            $item.removeAttr('src');
        });
        $lazyImgs = $('[data-url]');
        $lazyImgs.lazyload({
            data_attribute:"url",
            effect : "fadeIn",
            placeholder: "/static_v2/img/webapp/mall/info_placeholder.png"
        });
    });
}

function redirectTo(newHref) {
    var originalNewHref = newHref;
    var memberTokenQueryStrKey = 'fmt';
    var curRequestMemberToken = $.trim(W.curRequestMemberToken);

    if (curRequestMemberToken.length == 0) {
        newHref = newHref + ('&original=' + encodeURIComponent(originalNewHref));
        window.location.href = newHref;
        return;
    }

    var host = window.location.host;
    if(newHref && (newHref.match(/^(\.\/|\/)\S/g) || newHref.indexOf(host) >= 0) && (newHref.indexOf(memberTokenQueryStrKey+'=') > 0 )) {
        newHref = newHref.indexOf('?') >= 0 ? newHref + '&' + key + '=' + value : newHref + '?' + memberTokenQueryStrKey + '=' + curRequestMemberToken;
    }

    if (newHref.indexOf('woid') == -1 && newHref.indexOf('webapp_owner_id') == -1 && newHref.indexOf('module') == -1) {
        newHref = newHref + ('&original=' + encodeURIComponent(originalNewHref));
    }
    window.location.href = newHref;
}

function reload() {
    redirectTo(window.location.href);
}
