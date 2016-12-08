/**
 * Created by Pauline on 24/11/16.
 */
function tabOneClickHandler(e) {
    Enabler.counter('Click on Tab 1');
}
document.getElementById('tab-one').addEventListener('click',
tabOneClickHandler, false);