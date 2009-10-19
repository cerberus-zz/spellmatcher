jQuery.fn.jqCards = function(options) {
  
	zoomedCards = 0;
  
	settings = jQuery.extend({
		'position':[0,0],
		'cards':[],
		'thumbWidth':120,
		'thumbHeight':170,
		'zoomWidth':240,
		'zoomHeight':340
	}, options);

	$.sub.subscribe('card.zoomedIn', function(obj){
		$card = obj.src;
		$hand = obj.hand;
		
		zoomedCards++;
		
		$zoomed = $card.clone();
		$zoomed.css('position','absolute');
		
		var showZoomed = function(card, zoomed){
			card.before(zoomed);
			card.css('visibility','hidden');
			zoomed.css('top',card.position().top);
			zoomed.css('left',card.position().left);
			zoomed.css('z-index',zoomedCards);
		
			zoomed.show().animate({'width':settings.zoomWidth, 'height':settings.zoomHeight, 'top':parseInt(zoomed.css('top')) - settings.zoomHeight + settings.thumbHeight});

			zoomed.click(function(){
				zoomed = $(this);

				$.sub.publish('card.zoomedOut', {'hand':$hand, 'card':card, 'zoomed':zoomed});
			});
		}($card, $zoomed);
	});

	$.sub.subscribe('card.zoomedOut', function(obj){
		$hand = obj.hand;
		$card = obj.card;
		$zoomed = obj.zoomed;
		$zoomed.animate({'width':settings.thumbWidth, 'height':settings.thumbHeight, 'top':parseInt($zoomed.css('top')) + settings.zoomHeight - settings.thumbHeight}, function(){
					$card.css('visibility','visible');
					$card.show();
					$zoomed.remove();
				});
	});
	
	return this.each(function(){
		$hand = $(this);
		$hand.html('');

		$hand.css('position','absolute');
		$hand.css('left', settings.position[0] + 'px');
		$hand.css('top', settings.position[1] + 'px');
		$hand.css('width', ((settings.cards.length + 1) * settings.thumbWidth) + 'px');
		//$hand.css('width', '900px');
		
		$.each(settings.cards, function(){
			card = this;
			cardTitle = card.title;
			cardPath = card.src;
			$div = $('<div style="float:left;position:relative;"><div style="position:absolute;top:4px;right:4px;" class="toolbar"></div></div>');
			$toolbar = $('.toolbar', $div);
			$magnify = $('<img border="0" src="magnifier.png" />');
			$play = $('<img border="0" src="arrow_up.png" />');
			$tap = $('<img border="0" src="arrow_turn_right.png" />');
			$toolbar.append($magnify);
			$toolbar.append($play);
			$toolbar.append($tap);
			$magnify.click(function(){
				magnify = $(this);
				img = $('img.card', magnify.parent().parent());
				$.sub.publish('card.zoomedIn', {hand:$hand, src:img});
			});
			imgStyle = 'margin-left:2px; margin-right:2px; width:' + settings.thumbWidth + 'px; height:' + settings.thumbHeight + 'px;';
			$img = $('<img class="card" border="0" style="' + imgStyle + '" src="' + cardPath + '" title="' + cardTitle + '" />');
			$div.append($img)
			
			$hand.append($div);
		});
		
		
	});
};
