var gulp = require('gulp');
var sass = require('gulp-sass');
var concat = require('gulp-concat');

gulp.task('django', function() {
    const spawn = require('child_process').spawn;
    return spawn('python', ['bingo/manage.py', 'runserver'])
        .stderr.on('data', (data) => {
        console.log(`${data}`);
    });
});

gulp.task('styles', function() {
    gulp.src('./bingo/**/main.sass')
        .pipe(sass().on('error', sass.logError))
        .pipe(concat('style.css'))
        .pipe(gulp.dest('./bingo/home/static/css/'));
});

gulp.task('watch-sass', function() {
    gulp.watch('./bingo/home/static/sass/**/*.sass',['styles']);
})

gulp.task('default', ['django', 'watch-sass']);
