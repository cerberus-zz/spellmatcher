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
		//$hand.css('width', (settings.cards.length * settings.thumbWidth) + 'px');
		$hand.css('width', '900px');

		console.info($hand);
		
		$.each(settings.cards, function(){
			card = this;
			cardTitle = card.title;
			cardPath = card.src;
			imgStyle = 'margin-left:2px; margin-right:2px; width:' + settings.thumbWidth + 'px; height:' + settings.thumbHeight + 'px;';
			$img = $('<img border="0" style="' + imgStyle + '" src="' + cardPath + '" title="' + cardTitle + '" />');
			$img.click(function(){
				img = $(this);
				$.sub.publish('card.zoomedIn', {hand:$hand, src:img});
			});
			$hand.append($img);
		});
		
		
	});
};
