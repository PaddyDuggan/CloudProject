const { expect } = require('chai');
const { classifyIP, server } = require('./server');

describe('classifyIP', () => {
    after(() => {
        server.close(); // Close the server after all tests are done
    });

    it('should classify IPv4 addresses correctly', () => {
        expect(classifyIP('192.168.1.1')).to.equal('IPv4');
        expect(classifyIP('10.0.0.1')).to.equal('IPv4');
    });

    it('should classify IPv6 addresses correctly', () => {
        expect(classifyIP('2001:0db8:85a3:0000:0000:8a2e:0370:7334')).to.equal('IPv6');
        expect(classifyIP('::1')).to.equal('IPv6');
    });

    it('should classify unknown formats correctly', () => {
        expect(classifyIP('')).to.equal('Unknown');
        expect(classifyIP('1234')).to.equal('Unknown');
    });
});
