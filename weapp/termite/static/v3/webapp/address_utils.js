function initSessionStorage(){
    var s = sessionStorage;
    if (s.mallSessionStorageHasInit == 1|| W.projectId) {
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

/**
 * 收货地址来源URL：
 * 从编辑订单或无地址跳转时设置或覆盖mallShipfromUrl，从个人中心进入则清空mallShipfromUrl
 */
function setMallShipfromUrl(url){
    if(url === undefined){
        url = '';
    }
    sessionStorage.mallShipfromUrl = url;
}

function checkShipInfosBeforeBuy(buy_url){
    if(!sessionStorage.ship_infos||sessionStorage.ship_infos.length<=2){
        setMallShipfromUrl(buy_url);
        window.location.href="./?woid=" + getWoid() +"&module=mall&model=address&action=add" +addFmt('fmt');
    }else{
            var ship_infos = JSON.parse(sessionStorage.ship_infos);
            var hasSelectedShip =  false
            for (var i in ship_infos) {
                if(ship_infos[i].is_selected == true){
                    hasSelectedShip = true;
                    break;
                }
            }
            if(hasSelectedShip){
                window.location.href = buy_url;
            } else {
                setMallShipfromUrl(buy_url);
                window.location.href = "./?woid=" + getWoid() +"&module=mall&model=address&action=list" +addFmt('fmt');
            }
    }
}
