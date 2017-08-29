# -*- mode: ruby -*-
# vi: set ft=ruby :

require 'etc'
require 'pathname'

Vagrant.configure("2") do |config|
    # define synced folders
    config.vm.synced_folder ".", "/home/vagrant/pwc-address-book-api"

    config.vm.define "pabapi" do |pabapi|
        # define virtualization provider
        pabapi.vm.provider "virtualbox"
        # define box
        pabapi.vm.box = "ubuntu/trusty64"

        config.vm.provider "virtualbox" do |v|
            # define RAM in MBs
            v.memory = 2048
            # define number of vCPUs
            v.cpus = 2
        end
    end

    # forward SSH agent
    config.ssh.forward_agent = true
    config.ssh.insert_key = false

    config.vm.network :forwarded_port, guest: 22, host: 2401, id: "ssh", auto_correct: false
    config.vm.network :forwarded_port, guest: 3306, host: 3306, id: "mysql", auto_correct: false
    config.vm.network :forwarded_port, guest: 8000, host: 8000, id: "api", auto_correct: false
    config.vm.network :forwarded_port, guest: 5555, host: 5555, id: "gunicorn", auto_correct: false

    # provision with Ansible
    config.vm.provision :ansible do |ansible|
        ansible.playbook = "app-pwc-address-book-api.yaml"

        if ENV['ANSIBLE_TAGS'] != ""
            ansible.tags = ENV['ANSIBLE_TAGS']
        end

        ansible.extra_vars = {
            "app_pwc_address_book_api"=> {is_vagrant: true},
        }
    end
end
