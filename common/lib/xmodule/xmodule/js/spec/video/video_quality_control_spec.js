(function (undefined) {
    describe('VideoQualityControl', function () {
        var state, qualityControl, qualityControlEl, videoPlayer, player;

        afterEach(function () {
            $('source').remove();
            if (state.storage) {
                state.storage.clear();
            }
        });

        describe('constructor, YouTube mode', function () {
            beforeEach(function () {
                state =  jasmine.initializePlayerYouTube();
                qualityControl = state.videoQualityControl;
                videoPlayer = state.videoPlayer;
                player = videoPlayer.player;

                // Define empty methods in YouTube stub
                player.quality = 'large';
                player.setPlaybackQuality.andCallFake(function (quality){
                    player.quality = quality;
                });
            });

            it('contains the quality control and is initially hidden',
               function () {
                expect(qualityControl.el).toHaveClass(
                    'quality-control is-hidden'
                );
            });

            it('add ARIA attributes to quality control', function () {
                expect(qualityControl.el).toHaveAttrs({
                    'role': 'button',
                    'title': 'HD off',
                    'aria-disabled': 'false'
                });
            });

            it('bind the quality control', function () {
                expect(qualityControl.el).toHandleWith('click',
                    qualityControl.toggleQuality
                );

                expect(state.el).toHandle('play');
            });

            it('calls fetchAvailableQualities only once', function () {
                expect(player.getAvailableQualityLevels.calls.length)
                    .toEqual(0);

                videoPlayer.onPlay();
                videoPlayer.onPlay();

                expect(player.getAvailableQualityLevels.calls.length)
                    .toEqual(1);
            });

            it('shows the quality control on play if HD is available',
               function () {
                videoPlayer.onPlay();

                expect(qualityControl.el).not.toHaveClass('is-hidden');
            });

            it('leaves quality control hidden on play if HD is not available',
               function () {
                player.getAvailableQualityLevels.andReturn(
                    ['large', 'medium', 'small']
                );

                videoPlayer.onPlay();
                expect(qualityControl.el).toHaveClass('is-hidden');
            });

            it('switch to HD if it is available', function () {
                videoPlayer.onPlay();

                qualityControl.quality = 'large';
                qualityControl.el.click();
                expect(player.setPlaybackQuality)
                    .toHaveBeenCalledWith('highres');

                qualityControl.quality = 'highres';
                qualityControl.el.click();
                expect(player.setPlaybackQuality).toHaveBeenCalledWith('large');
            });
        });

        describe('constructor, HTML5 mode', function () {
            it('does not contain the quality control', function () {
                state =  jasmine.initializePlayer();

                expect(state.el.find('a.quality-control').length).toBe(0);
            });
        });
    });
}).call(this);
