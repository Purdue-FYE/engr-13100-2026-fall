/* Set --sch-sticky-top to the bottom of the last sticky header bar so that
   the schedule table's sticky thead doesn't slide under it. */
function updateSchStickyTop() {
    const bar = document.querySelector('.header-article-items');
    const top = bar ? bar.getBoundingClientRect().bottom : 0;
    document.documentElement.style.setProperty('--sch-sticky-top', top + 'px');
}
document.addEventListener('DOMContentLoaded', updateSchStickyTop);
window.addEventListener('resize', updateSchStickyTop);
