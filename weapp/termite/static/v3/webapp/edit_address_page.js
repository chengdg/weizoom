function initSessionStorage(){
    var s = sessionStorage;
    if (s.mallSessionStorageHasInit == 1) {
        return
    }else {
        var woid = getWoid();
        W.getApi().call({
            app: 'webapp',
            api: 'project_api/call',
            args: {
                woid: woid,
                module: 'mall',
                target_api: 'sessionstorage/init'
            },
            success: function(data) {
                sessionStorage.ship_infos=JSON.stringify(data.ship_infos);
                s.mallSessionStorageHasInit = 1;

            },
            error: function(resp) {
            }
        });
    }
}

function checkShipInfosBeforeBuy(buy_url){
    sessionStorage.mallShipfromUrl = buy_url;
    if(!sessionStorage.ship_infos||sessionStorage.ship_infos.length<=2){
        window.location.href="./?woid=" + getWoid() +"&module=mall&model=address&action=add" +addFmt('fmt');
    }else {
        window.location.href = buy_url;
    }
}


function returnOrder(){
    var mallShipfromUrl = sessionStorage.mallShipfromUrl;
    sessionStorage.removeItem('mallShipfromUrl');
    window.location.href = mallShipfromUrl;
}

/**
 * Backbone View in Mobile
 */
W.page.EditAddressPage = W.page.InputablePage.extend({
    events: _.extend({
        'click .xa-submit': 'onClickSubmitButton',
        'click .xa-delete':'onClickDeleteButton'
    }, W.page.InputablePage.prototype.events),

    /**
     * onClickSubmitButton: 点击“提交”按钮的响应函数
     */
    onClickSubmitButton: function(event) {
        var $form = $('form');
        if (W.validate($form)) {
            $('.xa-submit').attr('disabled','disabled');

            var args = $form.serializeObject();
            var ship_info = deepCopyJSON(args);
            ship_info['area_str'] = $('.xa-openSelect').text();

            W.getApi().call({
                app: 'webapp',
                api: 'project_api/call',
                method: 'post',
                args: _.extend(args, {
                    woid: W.webappOwnerId,
                    module: 'mall',
                    target_api: 'address/save'
                }),
                success: function(data) {
                    var ship_id = data['ship_id'];
                    ship_info['ship_id'] = ship_id;
                    ship_info['is_selected'] = true;
                    var ship_infos;
                    if(sessionStorage.ship_infos){
                        ship_infos = JSON.parse(sessionStorage.ship_infos);

                    }
                    else{
                        ship_infos = JSON.constructor();
                    }

                    for(var i in ship_infos){
                        if(i!=ship_id){
                            ship_infos[i].is_selected = false;

                        }
                    }
                    ship_infos[ship_id] = ship_info;

                    sessionStorage.ship_infos = JSON.stringify(ship_infos);


                    if (data['msg'] != null) {
                        $('body').alert({
                            isShow: true,
                            speed: 2000,
                            isSlide: true,
                            info: data['msg']
                        })
                    } else {
                        if(sessionStorage.mallShipfromUrl){
                            // 返回订单
                            returnOrder();
                        }else{
                            // 返回地址列表
                            window.location.href = document.referrer;
                        }
                    }
                },
                error: function(resp) {
                    var errMsg = '保存失败';
                    if (resp.errMsg) {
                        errMsg = resp.errMsg;
                    } else if (resp.data && resp.data['msg']) {
                        errMsg = resp.data['msg']
                    }

                    $('body').alert({
                        isShow: true,
                        isSlide: true,
                        info: errMsg,
                        speed: 2000
                    });
                }
            });
        } else {
            
        }
    },


    /**
     * onClickDeleteButton: 点击“删除”按钮的响应函数
     */
    onClickDeleteButton: function(event){
        var ship_id = getParam('id');
        W.getApi().call({
                app: 'webapp',
                api: 'project_api/call',
                method: 'post',
                args: {
                    woid: W.webappOwnerId,
                    module: 'mall',
                    target_api: 'address/delete',
                    id: ship_id
                },
                success: function(data) {
                    var selected_id=data.selected_id;

                    var ship_infos = JSON.parse(sessionStorage.ship_infos);
                    delete ship_infos[ship_id];
                    if(selected_id){
                        ship_infos[selected_id]['is_selected'] = true;
                    }
                    sessionStorage.ship_infos = JSON.stringify(ship_infos);
                    window.location.href = './?woid=' + getWoid()+ '&module=mall&model=address&action=list' + addFmt();

                },
                error: function(resp) {
                    var errMsg = '删除失败';
                    if (resp.errMsg) {
                        errMsg = resp.errMsg;
                    } else if (resp.data && resp.data['msg']) {
                        errMsg = resp.data['msg']
                    }

                    $('body').alert({
                        isShow: true,
                        isSlide: true,
                        info: errMsg,
                        speed: 2000
                    });
                }
            });



    }
});
