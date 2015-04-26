var myMap;

// Дождёмся загрузки API и готовности DOM.
ymaps.ready(init);

function init () {
    // Создание экземпляра карты и его привязка к контейнеру с
    // заданным id ("map").
    var myPlacemark,
    myMap = new ymaps.Map('map', {
        // При инициализации карты обязательно нужно указать
        // её центр и коэффициент масштабирования.
        center: [55.76, 37.64], // Москва
        zoom: 10,
        controls: []
    });

    // Создадим экземпляр элемента управления «поиск по карте», 
    // с установленной опцией провайдера данных для поиска по организациям.
    var searchControl = new ymaps.control.SearchControl({
        options: {
            provider: 'yandex#search'
        }
    });
    
    myMap.controls.add(searchControl);
    
    // Слушаем клик на карте
    myMap.events.add('click', function (e) {
        var coords = e.get('coords');
        console.log(coords);


        // Если метка уже создана – просто передвигаем ее
        if (myPlacemark) {
            myPlacemark.geometry.setCoordinates(coords);
        }
        // Если нет – создаем.
        else {
            myPlacemark = createPlacemark(coords);
            myMap.geoObjects.add(myPlacemark);
            // Слушаем событие окончания перетаскивания на метке.
            myPlacemark.events.add('dragend', function () {
                getAddress(myPlacemark.geometry.getCoordinates());
            });
        }
        getAddress(coords);
    });

    // Создание метки
    function createPlacemark(coords) {
        return new ymaps.Placemark(coords, {
            iconContent: 'поиск...'
        }, {
            preset: 'islands#violetStretchyIcon',
            draggable: true
        });
    }

    // Определяем адрес по координатам (обратное геокодирование)
    function getAddress(coords) {
        myPlacemark.properties.set({
                    iconContent: 'поиск...'
                });
        
        var area;
        str = "http://maps.googleapis.com/maps/api/geocode/json?latlng=" + coords
        var callback = function (address) {
            console.log(address);
            area = address["locality"];
            if(area === "Москва") {
                area = address["sublocality_level_1"]
                full_address = area + ", Москва";
            } else {
                full_address = address["locality"] + ", " + address["administrative_area_level_2"] + ", " + address["administrative_area_level_1"]
            }
               myPlacemark.properties
                .set({
                    iconContent: area,
                    balloonContent: area
                });
                // searchControl.search(full_address);
                $("#location").val(area);
        }

        var parseGoogleGeocoderResponse = function(res) {
            address_components = res["results"][0]["address_components"];
            console.log(address_components);
            var address = {};
            $.each(address_components, function (i, component) {
                console.log(component);
                types = component["types"];
                if($.inArray("locality", types) !== -1) {
                    console.log("bingo");
                    address["locality"] = component["long_name"];
                } else if ($.inArray("sublocality_level_1", types) !== -1) {
                    address["sublocality_level_1"] = component["long_name"];
                } else if ($.inArray("administrative_area_level_1", types) !== -1) {
                    address["administrative_area_level_1"] = component["long_name"];
                } else if ($.inArray("administrative_area_level_2", types) !== -1) {
                    address["administrative_area_level_2"] = component["long_name"];
                }
            
            })
            
            callback(address);
            
        }
        response = $.getJSON(str).then(parseGoogleGeocoderResponse);
        
        
    }
    
    document.getElementById('destroyButton').onclick = function () {
        // Для уничтожения используется метод destroy.
        myMap.destroy();
    };

    $("#getRecommendations").click(function () {
        var uid = $.data(document.body, "uid");
        console.log(uid);
        $.post("/", { "from": "Долгопрудный", "to": "Москва", "uid": uid }, function(res) {console.log(res); $('body').html(res)});
    })

}
