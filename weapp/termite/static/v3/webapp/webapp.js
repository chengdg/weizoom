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


W.preloadImgsOnPage = function(option) {
    if (!option) return;
    $(function(){
        option.map(function(ele){
            var noLazy = {
                'imageNav': 20,
                'imageGroup': 0,
            };
            var module = ele['moduleName'];
            var tagId = ele['tagId'];
            var $itemsImg = $(tagId);
            if (_.isEmpty($itemsImg)) {
                return;
            }
            switch(module) {
                case 'imageDisplay':
                    $itemsImg.map(function(idx, item) {
                        var $item = $(item);
                        $item.attr('data-url', $item.attr('src'));
                        $item.removeAttr('src');
                    });
                    $lazyImgs = $('[data-url]');
                    lazyloadImg($lazyImgs, {threshold: 200});
                    break;
                case 'imageNav':
                    $itemsImg.map(function(idx, item) {
                        var $item = $(item);
                        if (idx > noLazy['imageNav']) {
                            $item.attr('data-url', $item.attr('src'));
                            $item.removeAttr('src');
                        }
                    });
                    $lazyImgs = $('[data-url]');
                    lazyloadImg($lazyImgs, {threshold: 200});
                    break;
                case 'imageGroup':
                    $itemsImg.map(function(idx, item) {
                        var $item = $(item);
                        var srcImg = $item.attr('src');
                        if (idx <= noLazy['imageGroup']) {
                            $item.attr('src', compressImgUrl(srcImg, '!/quality/75'));
                            $item.removeAttr('data-url');
                        } else {
                            $item.attr('data-url', compressImgUrl(srcImg, '!/quality/80'));
                            $item.attr('src', compressImgUrl(srcImg, '!/quality/10'));
                        }
                    });
                    $lazyImgs = $('[data-url]');
                    lazyloadImg($lazyImgs, {threshold: 400});
                    break;
                case 'productList':
                    $itemsImg.map(function(idx, item) {
                        var $item = $(item);
                        $item.attr('data-url', compressImgUrl($item.attr('src'), ""));
                        $item.removeAttr('src');
                    });
                    $lazyImgs = $('[data-url]');
                    lazyloadImg($lazyImgs, {threshold: 0});
                    break;
                default:
                    break;
            }
        });
    });
}

// 如果是upaiyun图片则增加压缩参数
function compressImgUrl(imgUrl, paramStr) {
    if (imgUrl) {
        var chaozhiKey = /chaozhi\.weizoom\.com/;
        // 遇到chaozhi.weizoom.com
        // 替换"/termite_static/upload/"为"/static/upload/"
        if (chaozhiKey.test(imgUrl)){
            imgUrl = imgUrl.replace('/termite_static/upload/','/static/upload/');
        }
        // 在又拍云里做
        var upaiyunKey = /upaiyun\.com/;
        // 替换"/termite_static/upload/"为"/static/upload/"
        if (upaiyunKey.test(imgUrl)){
            imgUrl = imgUrl.replace('/termite_static/upload/','/static/upload/');
        }
        // 压缩过, 清理压缩参数
        var idxCompressed = imgUrl.lastIndexOf('!/');
        if ( idxCompressed > -1) {
            imgUrl = imgUrl.substring(0, idxCompressed);
        }
        var compressStr = paramStr;
        if (compressStr != "" && upaiyunKey.test(imgUrl)){
            return [imgUrl, compressStr].join('');
        }
        return imgUrl;
    }
}

function lazyloadImg($imgs, options) {
    var defOptions = {
            data_attribute:"url",
            skip_invisible : false,
            //effect : "fadeIn",
            placeholder: "/static_v2/img/webapp/mall/info_placeholder.png",
            failurelimit: 10
        };

    var options = _.defaults(options, defOptions);

    if ($imgs) {
        $imgs.lazyload(options);
    }
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
