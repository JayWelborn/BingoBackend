var gulp = require('gulp');
var sass = require('gulp-sass');
var concat = require('gulp-concat');
var postcss      = require('gulp-postcss');
var sourcemaps   = require('gulp-sourcemaps');
var autoprefixer = require('autoprefixer');

// Start Django server
gulp.task('django', function() {
    const spawn = require('child_process').spawn;
    return spawn('python', ['bingo/manage.py', 'runserver'])
        .stderr.on('data', (data) => {
        console.log(`${data}`);
    });
});

// Process sass files and output prefixed css
gulp.task('styles', function() {
    gulp.src('./bingo/**/main.sass')
        .pipe(sass().on('error', sass.logError))
        .pipe(concat('style.css'))
        .pipe(sourcemaps.init())
        .pipe(postcss([autoprefixer() ]))
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest('./bingo/home/static/css/'));
});

// gulp.task('autoprefixer', function () {
//     var postcss      = require('gulp-postcss');
//     var sourcemaps   = require('gulp-sourcemaps');
//     var autoprefixer = require('autoprefixer');

//     return gulp.src('./bingo/home/static/css/style.css')
//         .pipe(sourcemaps.init())
//         .pipe(postcss([ autoprefixer() ]))
//         .pipe(sourcemaps.write('.'))
//         .pipe(gulp.dest('./dest'));
// });

gulp.task('watch-sass', function() {
    gulp.watch('./bingo/home/static/sass/**/*.sass', ['styles']);
});

gulp.task('default', ['django', 'watch-sass']);
