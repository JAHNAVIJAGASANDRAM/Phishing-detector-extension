const fs = require('fs');
const sharp = require('sharp');

const svgFiles = [
    'icon16.svg',
    'icon48.svg',
    'icon128.svg',
    'icon16_warning.svg',
    'icon48_warning.svg',
    'icon128_warning.svg'
];

async function convertSvgToPng(svgFile) {
    const pngFile = svgFile.replace('.svg', '.png');
    const svgContent = fs.readFileSync(svgFile, 'utf-8');
    
    try {
        await sharp(Buffer.from(svgContent))
            .png()
            .toFile(pngFile);
        console.log(`Converted ${svgFile} to ${pngFile}`);
    } catch (error) {
        console.error(`Error converting ${svgFile}:`, error);
    }
}

async function convertAll() {
    for (const file of svgFiles) {
        await convertSvgToPng(file);
    }
}

convertAll().then(() => console.log('All conversions complete')); 