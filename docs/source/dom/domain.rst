********************************************
``libvirt_vmcfg.dom.domain``: domain builder
********************************************

.. py:module:: libvirt_vmcfg.dom.domain

This is the module containing the domain builder, which builds the XML sheet
out of Python objects. :py:class:`~libvirt_vmcfg.dom.elements.Element`
subclasses are attached to :py:class:`Domain` classes to build the final XML
sheet.

For convenience, all of these methods are imported into the
:py:mod:`~libvirt_vmcfg.dom` module directly as aliases.

########
Synopsis
########
The domain builder assists in building the actual XML. At the root of the
builder is a :py:class:`Domain` object. This on its own is not useful, but
by attaching :py:class:`~libvirt_vmcfg.dom.elements.Element` subclasses to
the object, the XML can be built in a much more Pythonic way than working
with the raw XML.

##################
Domain builder API
##################

==========
DomainType
==========
.. py:class:: DomainType

   :synopsis: An :py:class:`~enum.Enum` containing the types of known
              domain hypervisor types.

   .. py:attribute:: KVM
      :value: "kvm"

      Denotes a KVM domain.

   .. todo:: Support other domain types, such as Xen.


======
Domain
======
.. py:class:: Domain(type: DomainType = DomainType.KVM, \
                     elements : Optional[Sequence[Element]] = None)

   :synopsis: The basic domain builder class, which elements are attached to.

   :param DomainType type: The type of domain.
   :param Sequence elements: A sequence of :py:class:`Element` subclasses to
                             construct the class with. If ``None``, then it
                             will be constructed with an empty list.
   :raises ValueError: if data passed in is invalid
   :raises: possibly other element-specific exceptions, if elements are passed
            in.
   
   .. warning:: In a future version KVM will not be the default domain type.

   .. py:attribute:: type
      :type: DomainType

      The :py:class:`DomainType` of this :py:class:`Domain`.

   .. py:attribute:: root
      :type: lxml.etree._Element

      The root lxml etree node, always an :py:class:`~lxml.etree._Element`
      object.

      .. warning:: Use caution when directly manipulating XML nodes in the
                   root. You may have to update the corresponding tag in
                   the :py:attr:`~Domain.elements` attribute.

   .. py:attribute:: elements

      A list of named tuples, giving the XML tags and associated
      :py:class:`Element` classes.

      .. warning:: This is an implementation detail and is best left alone
                   unless you are sure you know what you're doing.

   .. :py:method:: attach_element(element: Element) -> ElementData

      :param Element element: A subclass of :py:class:`Element` to attach to
                              the domain.
      :return: An ElementData structure that can be passed to
               :py:meth:`~Domain.detach_element`.

      Attach a subclass of :py:class:`Element` to this domain.

      Use :py:method:`detach_element` to detach an element.

   .. :py:method:: detach_element(data: ElementData) -> None

      :param ElementData data: Item returned from
                               :py:meth:`~Domain.attach_element`
   
      Detach an element from this domain.

   .. :py:method:: emit_xml(*, pretty_print: bool = False, \
                            encoding: str = "unicode") -> Union[str, bytes]

      :param bool pretty_print: Whether or not the resulting text should be
                                formatted for pretty printing.
      :param str encoding: The encoding of the resulting XML string emitted,
                           if set to ``None``, ``bytes`` will be emitted.

      Emit XML based on the built elements so far.

      This method is :wikipedia-en:`idempotent <Idempotence>`.
