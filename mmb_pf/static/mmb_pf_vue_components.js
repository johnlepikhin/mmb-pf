const { reactiveProp } = VueChartJs.mixins;
let BlueMapGallery = Vue.component('blue-map-gallery', {
    template : `
        <div
            :id="id"
            class="blueimp-gallery blueimp-gallery-controls"
            :class="{'blueimp-gallery-carousel': carousel}">
            <div class="slides"></div>
            <h3 class="title"></h3>
            <a class="prev">
                <slot name="prev">‹</slot>
            </a>
            <a class="next">
                <slot name="next">›</slot>
            </a>
            <p class="description"></p>
            <a v-if="!carousel" class="close">
                <slot name="close">X</slot>
            </a>
            <ol v-if="!carousel" class="indicator"></ol>
            <a v-if="!carousel" class="play-pause"></a>
        </div>
    `,
    props: {
        images: {
            type: Array,
            default() {
                return [];
            }
        },
        options: {
            type: Object,
            default() {
                return {};
            }
        },
        carousel: {
            type: Boolean,
            default: false
        },
        index: {
            type: Number
        },
        id: {
            type: String,
            default: "blueimp-gallery"
        }
    },
    data() {
        return {
            instance: null
        };
    },
    watch: {
        index(value) {
            if (this.carousel) {
                return;
            }
            if (value !== null) {
                this.open(value);
            } else {
                if (this.instance) {
                    this.instance.close();
                }
                this.$emit("close");
            }
        }
    },
    mounted() {
        if (this.carousel) {
            this.open();
        }
    },
    destroyed() {
        if (this.instance !== null) {
            this.instance.destroyEventListeners();
            this.instance.close();
            this.instance = null;
        }
    },
    methods: {
        open(index = 0) {
            const instance = typeof blueimp.Gallery !== "undefined" ? blueimp.Gallery : blueimp;
            const options = Object.assign(
                {
                    toggleControlsOnReturn: false,
                    stretchImages: false,
                    toggleControlsOnSlideClick: false,
                    closeOnSlideClick: false,
                    carousel: this.carousel,
                    container: `#${this.id}`,
                    index,
                    onopen: () => this.$emit("onopen"),
                    onopened: () => this.$emit("onopened"),
                    onslide: this.onSlideCustom,
                    onslideend: (index, slide) => this.$emit("onslideend", { index, slide }),
                    onslidecomplete: (index, slide) => this.$emit("onslidecomplete", { index, slide }),
                    onclose: () => this.$emit("close"),
                    onclosed: () => this.$emit("onclosed")
                },
                this.options
            );
            if (this.carousel) {
                options.container = this.$el;
            }
            this.instance = instance(this.images, options);
        },
        onSlideCustom(index, slide) {
            this.$emit("onslide", { index, slide });
            const image = this.images[index];
            if (image !== undefined) {
                const text = image.desc;
                const node = this.instance.container.find(".description");
                if (text) {
                    node.empty();
                    node[0].appendChild(document.createTextNode(text));
                }
            }
        }
    },
});
let ESSGallery = Vue.component('ess-gallery', {
    delimiters: ['-*', '*-'],
    template : `
    <div class="ess-gallery">
        <div class="inner-banner-outer pt-0" v-if="images != undefined && images.length > 0">
            <div class="col-12 img-main" v-if="images.length >= 5">
                <div class="row">
                    <blue-map-gallery :images="images" :index="index" @close="index = null"></blue-map-gallery>
                    <div
                        @click="index = 0"
                        class="col-6 p-0 img-left"
                        :style="{ backgroundImage: 'url(' + images[0].href + ')' }"
                    ></div>
                    <div class="col-md-6 col-sm-12 p-0">
                        <div class="row m-0">
                            <div v-for="n in 4" :key="n" @click="index = n" class="col-md-6 col-sm-12 p-0 img-right" :style="{ backgroundImage: 'url(' + images[n].href + ')' }">
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="p-0 col-12 img-main" v-else>
            <blue-map-gallery :images="images" :index="index" @close="index = null"></blue-map-gallery>
            <div
                @click="index = 0"
                class="img-left"
                :style="{ backgroundImage: 'url(' + images[0].href + ')' }">
            </div>
            </div>
            <div class="col-12 text-right more-btn-main">
                <button @click="index = 0" class="btn more-btn">Просмотр</button>
            </div>
        </div>
    </div>`,
    props: {
        images: {
            type: Array,
            default() {
                return [];
            },
        },
    },
    data: function () {
        return {
            index: null
        };
    },
    components:{
        'blue-map-gallery': BlueMapGallery,
    },
    methods: {

    },
    mounted () {

    },
    watch: {

    }
});
let ChartLineStacked = Vue.component('chart-line-stacked', {
    extends: VueChartJs.Line,
    mixins: [reactiveProp],
    props: ['chartData'],
    data: function () {
        return {
            options: {
                maintainAspectRatio: false,
                scales: {
                    xAxes: [{
                        stacked: true
                    }],
                    yAxes: [{
                        stacked: true
                    }]
                },
                spanGaps: true,
                elements: {
                    line: {
                        tension: 0.04
                    }
                },
                plugins: {
                    filler: {
                        propagate: true
                    },
                },
                legend: {
                    display: true,
                },
                tooltips: {
                    callbacks: {
                        title: function() {
                            return "";
                        },
                        label: function(item, data) {
                            // console.log(item);
                            // console.log(data);
                            let resultTooltip = ['Этап: ' + item.xLabel];
                            let all_points = 0;
                            data.datasets.some(function(obj) {
                                all_points += obj.data[item.index];
                            });

                            let datasetPct = Math.round(item.value * 100 / all_points);
                            resultTooltip.push(data.datasets[item.datasetIndex].label + ': ' + item.yLabel + ' ('+ datasetPct + ' %)');
                            return resultTooltip;
                        }
                    }
                }
            }
        }
    },
    methods: {
        renderStackedLineChart: function () {
            this.renderChart(this.chartData, this.options);
        },
    },
    mounted () {
        this.renderStackedLineChart();
    },
    watch: {
        chartData: function() {
            this.renderStackedLineChart();
        }
    }
});

let ChartDoughnut = Vue.component('chart-doughnut', {
    extends: VueChartJs.Doughnut,
    props: ['chartData', 'сhartTitle'],
    data: function () {
        return {
            options: {
                responsive: true,
                maintainAspectRatio: false,
                title: {
                    display: true,
                    text: this.сhartTitle,
                },
                legend: {
                    position: 'bottom',
                    labels: {
                        boxWidth: 8,
                    },
                },
                tooltips: {
                    callbacks: {
                        title: function() {
                            return "";
                        },
                        label: function(item, data) {
                            // console.log(item);
                            // console.log(data);
                            let resultTooltip = [data.labels[item.index]];
                            let all_points = 0;
                            data.datasets[item.datasetIndex].data.some(function(val) {
                                all_points += val;
                            });

                            let datasetPct = Math.round(data.datasets[item.datasetIndex].data[item.index] * 100 / all_points);
                            resultTooltip.push('Кол-во: ' + data.datasets[item.datasetIndex].data[item.index] + ' ('+ datasetPct + ' %)');
                            return resultTooltip;
                        }
                    }
                }
            }
        }
    },
    methods: {
        renderDoughnutChart: function () {
            this.renderChart(this.chartData, this.options);
        },
    },
    mounted() {
        this.renderDoughnutChart();
    },
    watch: {
        chartData: function() {
            this.renderDoughnutChart();
        }
    },
});

let ChartBarStacked = Vue.component('chart-bars-stacked', {
    extends: VueChartJs.Bar,
    mixins: [reactiveProp],
    props: ['chartData',],
    data: function () {
        return {
            options: {
                maintainAspectRatio: false,
                scales: {
                    xAxes: [{
                        stacked: true
                    }],
                    yAxes: [{
                        stacked: true
                    }]
                },
                spanGaps: true,
                elements: {
                    line: {
                        tension: 0.04
                    }
                },
                plugins: {
                    filler: {
                        propagate: true
                    },
                },
                legend: {
                    display: true,
                },
                tooltips: {
                    callbacks: {
                        title: function() {
                            return "";
                        },
                        label: function(item, data) {
                            // console.log(item);
                            // console.log(data);
                            let resultTooltip = [item.xLabel];
                            let all_points = 0;
                            data.datasets.some(function(obj) {
                                all_points += obj.data[item.index];
                            });

                            let datasetPct = Math.round(item.value * 100 / all_points);
                            resultTooltip.push(data.datasets[item.datasetIndex].label + ': ' + item.yLabel + ' ('+ datasetPct + ' %)');
                            return resultTooltip;
                        }
                    }
                }
            }
        }
    },
    methods: {
        renderStackedLineChart: function () {
            this.renderChart(this.chartData, this.options);
        },
    },
    mounted () {
        this.renderStackedLineChart();
    },
    watch: {
        chartData: function() {
            this.renderStackedLineChart();
        }
    }
});